import json
from datetime import datetime
from collections import defaultdict
import os
import glob
from neo4j import GraphDatabase

# TODO clean this up
# Neo4j settings
neo4j_uri = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
neo4j_user = os.getenv("NEO4J_USER", "neo4j")
neo4j_password = os.getenv("NEO4J_PASSWORD", "Pass@word")

# Initialize Neo4j driver
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))


def update_node_graph(log_directory):
    latest_log_file = _get_latest_log_file(log_directory)
    events = _read_events(latest_log_file)
    _update_neo4j_node_graph(events)

    return events

def _update_neo4j_node_graph(events: dict):

    for key, event in events.items():

        if (event['stream_object_id'] is None):
            continue

        with driver.session() as session:
            session.write_transaction(_merge_stream_object, event)
            session.write_transaction(_merge_sh_and_so_edge, event)

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


def _read_events(log_file_path):
    events = defaultdict(lambda: {
        'count': 0,
        'timestamp': None,
        'data_stream_id': None,
        'data_stream_name': None,
        'stream_object_id': None,
        'stream_object_name': None,
        'stream_object_type': None,
        'stream_host_id': None,
        'stream_host_name': None,
        'collection_id': None
    })

    with open(log_file_path, 'r') as file:
        for line in file:
            try:
                log_entry = json.loads(line)
                properties = log_entry.get('Properties', {})

                stream = properties.get('Stream', {})
                agent = properties.get('Agent', {})
                host = properties.get('Host', {})

                key = str(agent.get('Id'))

                events[key]['count'] += 1
                events[key]['timestamp'] = log_entry['Timestamp']
                events[key]['data_stream_id'] = stream.get('Id')
                events[key]['data_stream_name'] = stream.get('Name')
                events[key]['stream_object_id'] = agent.get('Id')
                events[key]['stream_object_name'] = agent.get('Name')
                events[key]['stream_object_type'] = agent.get('Type')
                events[key]['stream_host_id'] = host.get('DeviceId')
                events[key]['stream_host_name'] = host.get('Name')
                events[key]['collection_id'] = host.get('CollectionId')

            except json.JSONDecodeError:
                print(f"Error decoding JSON from line: {line}")
            except KeyError as e:
                print(f"KeyError: {e} in line: {line}")

    return dict(events)


def _merge_stream_object(tx, event):
    query = """
    MERGE (so:StreamObject {id: $so_id})
    SET so.title = $so_title,
        so.type = $so_type,
        so.event_count = $so_event_count,
        so.last_updated = $last_updated
    """

    tx.run(query, {
        "so_id": event['stream_object_id'],
        "so_title": event['stream_object_name'],
        "so_type": event['stream_object_type'],
        "so_event_count": event['count'],
        "log_created": event['timestamp'],
        "last_updated": datetime.now().isoformat()
    })



def _merge_sh_and_so_edge(tx, event):
    query = """
        MATCH (so:StreamObject {id: $so_id})
    
        MERGE (sh:StreamHost {id: $sh_id})
        SET sh.title = $sh_title,
            sh.last_updated = $last_updated

        WITH so, sh

        MERGE (sh)-[shr:EXECUTED { 
                id: $sh_rel_id, 
                source_id: $sh_id,
                target_id: $so_id,
                last_updated: $last_updated
            }]->(so)
    """

    tx.run(query, {
        "so_id": event['stream_object_id'],
        "sh_rel_id": event['stream_host_id'] + "_" + event['stream_object_id'],
        "sh_id": event['stream_host_id'],
        "sh_title": event['stream_host_name'],
        "log_created": event['timestamp'],
        "last_updated": datetime.now().isoformat(),
    })