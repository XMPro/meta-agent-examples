import json
from datetime import datetime
from collections import defaultdict
import os
import glob


def foo():
    return "bar"


def update_node_graph(log_directory):
    latest_log_file = _get_latest_log_file(log_directory)
    events = _read_events(latest_log_file)
    # _update_neo4j_node_graph(events)

    # Print results
    # for key, event in event_counts.items():
    #     print(f"\nStream Object: {key}")
    #     print(f"  Count: {event['count']}")
    #     print(f"  Last Updated: {event['last_updated']}")
    #     print(f"  Data Stream ID: {event['data_stream_id']}")
    #     print(f"  Data Stream Name: {event['data_stream_name']}")
    #     print(f"  Stream Object ID: {event['stream_object_id']}")
    #     print(f"  Stream Object Name: {event['stream_object_name']}")
    #     print(f"  Stream Object Type: {event['stream_object_type']}")
    #     print(f"  SH ID: {event['sh_id']}")
    #     print(f"  SH Name: {event['sh_name']}")
    #     print(f"  SH Collection ID: {event['sh_collection_id']}")

    return events


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


def parse_timestamp(timestamp_str):
    """
    Parse timestamp string to datetime object, handling various ISO format variations.
    """
    try:
        # Try parsing with microseconds
        return datetime.fromisoformat(timestamp_str)
    except ValueError:
        try:
            # If that fails, try stripping any subsecond precision beyond 6 digits
            # Split on decimal point
            main_part, subseconds = timestamp_str.rsplit('.', 1)
            timezone_split = subseconds.rsplit('+', 1)
            
            if len(timezone_split) > 1:
                subseconds, timezone = timezone_split
                # Truncate subseconds to 6 digits if longer
                subseconds = subseconds[:6]
                new_timestamp = f"{main_part}.{subseconds}+{timezone}"
            else:
                # Handle case where there's no explicit timezone
                subseconds = subseconds[:6]
                new_timestamp = f"{main_part}.{subseconds}"
                
            return datetime.fromisoformat(new_timestamp)
        except Exception as e:
            print(f"Error parsing timestamp '{timestamp_str}': {e}")
            # Return current time as fallback
            return datetime.now()


def _read_events(log_file_path):
    events = defaultdict(lambda: {
        'count': 0,
        'last_updated': None,
        'data_stream_id': None,
        'data_stream_name': None,
        'stream_object_id': None,
        'stream_object_name': None,
        'stream_object_type': None,
        'sh_id': None,
        'sh_name': None,
        'sh_collection_id': None
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
                timestamp = parse_timestamp(log_entry['Timestamp'])

                if events[key]['last_updated'] is None or timestamp > events[key]['last_updated']:
                    events[key]['last_updated'] = timestamp

                events[key]['data_stream_id'] = stream.get('Id')
                events[key]['data_stream_name'] = stream.get('Name')
                events[key]['stream_object_id'] = agent.get('Id')
                events[key]['stream_object_name'] = agent.get('Name')
                events[key]['stream_object_type'] = agent.get('Type')
                events[key]['sh_id'] = host.get('DeviceId')
                events[key]['sh_name'] = host.get('Name')
                events[key]['sh_collection_id'] = host.get('CollectionId')

            except json.JSONDecodeError:
                print(f"Error decoding JSON from line: {line}")
            except KeyError as e:
                print(f"KeyError: {e} in line: {line}")

    return dict(events)