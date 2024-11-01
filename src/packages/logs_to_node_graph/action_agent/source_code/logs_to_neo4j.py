import json
from datetime import datetime, timezone
from collections import defaultdict
import os
import glob
from neo4j import GraphDatabase

# Neo4j settings
neo4j_uri = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
neo4j_user = os.getenv("NEO4J_USER", "neo4j")
neo4j_password = os.getenv("NEO4J_PASSWORD", "Pass@word")

# Initialize Neo4j driver
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

LAST_PROCESSED_FILE = "last_processed_timestamp.txt"


def _get_last_processed_timestamp():
    try:
        with open(LAST_PROCESSED_FILE, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def _save_last_processed_timestamp(timestamp):
    with open(LAST_PROCESSED_FILE, 'w') as f:
        f.write(timestamp)


def _get_current_event_counts():
    with driver.session() as session:
        result = session.run("""
            MATCH (so:StreamObject)
            RETURN so.node_id as id, 
                so.event_count as event_count,
                so.event_complete_count as event_complete_count,
                so.event_failed_count as event_failed_count
        """)
        return {record["id"]: {
            "event_count": record["event_count"],
            "event_complete_count": record["event_complete_count"],
            "event_failed_count": record["event_failed_count"]
        } for record in result}


def update_node_graph(log_directory):
    latest_log_file = _get_latest_log_file(log_directory)
    last_timestamp = _get_last_processed_timestamp()

    # Get current counts from Neo4j
    current_counts = _get_current_event_counts()

    # Read only new events
    events, latest_timestamp = _read_events(
        latest_log_file, last_timestamp, current_counts)

    if events:
        _update_neo4j_node_graph(events)
        _save_last_processed_timestamp(latest_timestamp)

    return events


def _update_neo4j_node_graph(events: dict):
    with driver.session() as session:
        for key, event in events.items():
            if event['stream_object_id'] is None:
                continue

            session.write_transaction(_merge_stream_object, event)
            session.write_transaction(_merge_sh_and_ds_edge, event)
            session.write_transaction(_merge_collection_and_sh_edge, event)
            session.write_transaction(_merge_ds_and_sh_edge, event)
            # session.write_transaction(_merge_node_event_complete_count, event)


def _get_latest_log_file(log_directory, pattern="sh-log-*.json"):
    """
    Find the most recently created log file in the specified directory
    matching the given pattern.
    """
    log_files = glob.glob(os.path.join(log_directory, pattern))

    if not log_files:
        raise FileNotFoundError(f"No log files found matching pattern '{pattern}' in {log_directory}")

    latest_file = max(log_files, key=os.path.getctime)
    return latest_file


def _read_events(log_file_path, last_processed_timestamp, current_counts):
    events = defaultdict(lambda: {
        'timestamp': None,
        'data_stream_id': None,
        'data_stream_name': None,
        'stream_object_id': None,
        'stream_object_name': None,
        'stream_object_type': None,
        'stream_host_id': None,
        'stream_host_name': None,
        'collection_id': None,
        'stream_object_event_count': 0,
        'stream_object_event_complete_count': 0,
        'stream_object_event_failed_count': 0
    })

    # Initialize with current counts
    for so_id in current_counts.items():
        if so_id is not None:
            events[str(so_id)]['stream_object_event_count'] = current_counts[so_id]['event_count']
            events[str(so_id)]['stream_object_event_complete_count'] = current_counts[so_id]['event_complete_count']
            events[str(so_id)]['stream_object_event_failed_count'] = current_counts[so_id]['event_failed_count']

    latest_timestamp = last_processed_timestamp
    new_events_found = False

    # Count new events
    with open(log_file_path, 'r') as file:
        for line in file:
            try:
                log_entry = json.loads(line)
                timestamp = log_entry['Timestamp']

                # Skip if we've already processed this timestamp
                if last_processed_timestamp and timestamp <= last_processed_timestamp:
                    continue

                new_events_found = True
                properties = log_entry.get('Properties', {})
                stream = properties.get('Stream', {})
                agent = properties.get('Agent', {})
                host = properties.get('Host', {})

                so_id = agent.get('Id')
                is_stream_object_event = so_id is not None

                # TODO implement total elapsed time
                elapsed_time = properties.get('ElapsedTime')
                is_stream_object_event_completed = elapsed_time is not None and elapsed_time > 0

                level = log_entry.get('Level')
                is_stream_object_event_error = level == 'Error'

                if is_stream_object_event and (is_stream_object_event_completed or is_stream_object_event_error):
                    key = str(so_id)

                    event_count = events[key]['stream_object_event_count']
                    events[key]['stream_object_event_count'] = event_count + 1

                    events[key].update({
                        'timestamp': timestamp,
                        'stream_object_id': str(so_id),
                        'stream_object_name': agent.get('Name'),
                        'stream_object_type': agent.get('Type'),
                        'stream_host_id': str(host.get('DeviceId')),
                        'stream_host_name': host.get('Name'),
                        'collection_id': str(host.get('CollectionId')),
                        'data_stream_id': str(stream.get('Id')),
                        'data_stream_name': stream.get('Name'),
                        'stream_object_event_count': events[key]['stream_object_event_count'],
                    })

                    # Update latest timestamp
                    if latest_timestamp is None or timestamp > latest_timestamp:
                        latest_timestamp = timestamp

                    if is_stream_object_event_completed:
                        # Increment event complete count
                        event_complete_count = events[key]['stream_object_event_complete_count']
                        events[key]['stream_object_event_complete_count'] = event_complete_count + 1
                    elif is_stream_object_event_error:
                        event_failed_count = events[key].get(
                            'stream_object_event_failed_count', 0)
                        events[key]['stream_object_event_failed_count'] = event_failed_count + 1

            except json.JSONDecodeError:
                print(f"Error decoding JSON from line: {line}")
            except KeyError as e:
                print(f"KeyError: {e} in line: {line}")

    # If no new events were found, return empty dict
    if not new_events_found:
        return {}, latest_timestamp

    return dict(events), latest_timestamp


def _merge_stream_object(tx, event):
    # node_id is used instead of id due strange behavior with the id property
    # when using the kniepdennis-neo4j-datasource in grafana
    query = """
    MERGE (so:StreamObject {node_id: $so_id})
    SET so.title = $so_title,
        so.type = $so_type,
        so.event_complete_count = $so_event_complete_count,
        so.event_failed_count = $so_event_failed_count,
        so.log_created = $log_created,
        so.last_updated = $last_updated
    """

    tx.run(query, {
        "so_id": event['stream_object_id'],
        "so_title": event['stream_object_name'],
        "so_type": event['stream_object_type'],
        "so_event_complete_count": event['stream_object_event_complete_count'],
        "so_event_failed_count": event['stream_object_event_failed_count'],
        "log_created": event['timestamp'],
        "last_updated": datetime.now(timezone.utc).isoformat()
    })


def _merge_ds_and_sh_edge(tx, event):
    query = """
        MATCH (so:StreamObject {node_id: $so_id})
    
        MERGE (ds:DataStream {node_id: $ds_id})
        SET ds.title = $ds_title,
            ds.log_created = $log_created,
            ds.last_updated = $last_updated
        
        WITH so, ds
        
        MERGE (ds)-[dsr:CONTAINS { 
                id: $ds_rel_id
            }]->(so)
        ON CREATE SET dsr.source_id = $ds_id, 
            dsr.target_id = $so_id,
            dsr.last_updated = $last_updated
    """

    tx.run(query, {
        "so_id": event['stream_object_id'],
        "ds_id": event['data_stream_id'],
        "ds_title": event['data_stream_name'],
        "ds_rel_id": str(event['data_stream_id']) + "_" + str(event['stream_object_id']),
        "log_created": event['timestamp'],
        "last_updated": datetime.now(timezone.utc).isoformat()
    })


def _merge_sh_and_ds_edge(tx, event):
    query = """
        MATCH (ds:DataStream {node_id: $ds_id})
    
        MERGE (sh:StreamHost {node_id: $sh_id})
        SET sh.title = $sh_title,
            sh.log_created = $log_created,
            sh.last_updated = $last_updated

        WITH ds, sh

        MERGE (sh)-[shr:EXECUTED { 
                id: $sh_rel_id                
            }]->(ds)
        ON CREATE SET shr.source_id = $sh_id,
            shr.target_id = $ds_id,
            shr.last_updated = $last_updated
    """

    tx.run(query, {
        "ds_id": event['data_stream_id'],
        "sh_rel_id": str(event['stream_host_id']) + "_" + str(event['data_stream_id']),
        "sh_id": event['stream_host_id'],
        "sh_title": event['stream_host_name'],
        "log_created": event['timestamp'],
        "last_updated": datetime.now(timezone.utc).isoformat()
    })


def _merge_collection_and_sh_edge(tx, event):
    query = """
        MATCH (sh:StreamHost {node_id: $sh_id})
    
        MERGE (c:Collection {node_id: $collection_id})
        SET c.title = $collection_title,
            c.log_created = $log_created,
            c.last_updated = $last_updated

        WITH sh, c
        
        MERGE (c)-[cr:CONTAINS { 
                id: $collection_rel_id
            }]->(sh)
        ON CREATE SET cr.source_id = $collection_id, 
            cr.target_id = $sh_id,
            cr.last_updated = $last_updated
    """

    tx.run(query, {
        "sh_id": event['stream_host_id'],
        "collection_id": event['collection_id'],
        "collection_title": event['collection_id'],
        "collection_rel_id": str(event['collection_id']) + "_" + str(event['stream_host_id']),
        "log_created": event['timestamp'],
        "last_updated": datetime.now(timezone.utc).isoformat()
    })

# def _merge_node_event_complete_count(tx, event):
#     query = """
#     MERGE (so:StreamObject {node_id: $so_id})
#     SET so.event_complete_count = $so_event_complete_count,
#         so.last_updated = $last_updated
#     """

#     tx.run(query, {
#         "so_id": event['stream_object_id'],
#         "so_event_complete_count": event['stream_object_event_complete_count'],
#         "last_updated": datetime.now(timezone.utc).isoformat()
#     })
