# import json
# from datetime import datetime
# from collections import defaultdict
# import os
# import glob


def foo():
    return "bar"


# def update_node_graph(log_directory):
#     latest_log_file = _get_latest_log_file(log_directory)
#     print(f"Processing log file: {latest_log_file}")

#     # Count events from the latest file
#     event_counts = _count_events(latest_log_file)

#     # Print results
#     for key, event in event_counts.items():
#         print(f"\nStream Object: {key}")
#         print(f"  Count: {event['count']}")
#         print(f"  Last Updated: {event['last_updated']}")
#         print(f"  Data Stream ID: {event['data_stream_id']}")
#         print(f"  Data Stream Name: {event['data_stream_name']}")
#         print(f"  Stream Object ID: {event['stream_object_id']}")
#         print(f"  Stream Object Name: {event['stream_object_name']}")
#         print(f"  Stream Object Type: {event['stream_object_type']}")
#         print(f"  SH ID: {event['sh_id']}")
#         print(f"  SH Name: {event['sh_name']}")
#         print(f"  SH Collection ID: {event['sh_collection_id']}")

#     return event_counts


# def _get_latest_log_file(log_directory, pattern="sh-log-*.json"):
#     """
#     Find the most recently created log file in the specified directory
#     matching the given pattern.
#     """
#     # Get full path for all matching files
#     log_files = glob.glob(os.path.join(log_directory, pattern))

#     if not log_files:
#         raise FileNotFoundError(f"No log files found matching pattern '{
#                                 pattern}' in {log_directory}")

#     # Get the most recent file based on creation time
#     latest_file = max(log_files, key=os.path.getctime)
#     return latest_file


# def _count_events(log_file_path):
#     event_counts = defaultdict(lambda: {
#         'count': 0,
#         'last_updated': None,
#         'data_stream_id': None,
#         'data_stream_name': None,
#         'stream_object_id': None,
#         'stream_object_name': None,
#         'stream_object_type': None,
#         'sh_id': None,
#         'sh_name': None,
#         'sh_collection_id': None
#     })

#     with open(log_file_path, 'r') as file:
#         for line in file:
#             try:
#                 log_entry = json.loads(line)
#                 properties = log_entry.get('Properties', {})

#                 stream = properties.get('Stream', {})
#                 agent = properties.get('Agent', {})
#                 host = properties.get('Host', {})

#                 key = (agent.get('Id'), agent.get('Name'))

#                 event_counts[key]['count'] += 1
#                 timestamp = datetime.fromisoformat(
#                     log_entry['Timestamp'].replace('Z', '+00:00'))

#                 if event_counts[key]['last_updated'] is None or timestamp > event_counts[key]['last_updated']:
#                     event_counts[key]['last_updated'] = timestamp

#                 event_counts[key]['data_stream_id'] = stream.get('Id')
#                 event_counts[key]['data_stream_name'] = stream.get('Name')
#                 event_counts[key]['stream_object_id'] = agent.get('Id')
#                 event_counts[key]['stream_object_name'] = agent.get('Name')
#                 event_counts[key]['stream_object_type'] = agent.get('Type')
#                 event_counts[key]['sh_id'] = host.get('DeviceId')
#                 event_counts[key]['sh_name'] = host.get('Name')
#                 event_counts[key]['sh_collection_id'] = host.get(
#                     'CollectionId')

#             except json.JSONDecodeError:
#                 print(f"Error decoding JSON from line: {line}")
#             except KeyError as e:
#                 print(f"KeyError: {e} in line: {line}")

#     return dict(event_counts)


# def update_node_graph(log_file_path):
#     event_counts = _count_events(log_file_path)

#     for key, data in event_counts.items():
#         print(f"Stream Object: {key}")
#         print(f"  Count: {data['count']}")
#         print(f"  Last Updated: {data['last_updated']}")
#         print(f"  Data Stream ID: {data['data_stream_id']}")
#         print(f"  Data Stream Name: {data['data_stream_name']}")
#         print(f"  Stream Object ID: {data['stream_object_id']}")
#         print(f"  Stream Object Name: {data['stream_object_name']}")
#         print(f"  Stream Object Type: {data['stream_object_type']}")
#         print(f"  SH ID: {data['sh_id']}")
#         print(f"  SH Name: {data['sh_name']}")
#         print(f"  SH Collection ID: {data['sh_collection_id']}")
#         print()
