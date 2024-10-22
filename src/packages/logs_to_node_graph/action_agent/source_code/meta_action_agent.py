# TODO include example of this
from src.packages.logs_to_node_graph.action_agent.source_code.logs_to_neo4j import update_node_graph
import os
import json
from datetime import datetime
from collections import defaultdict
import glob
from neo4j import GraphDatabase

# Global variables
stream_object_id = None
stream_object_title = None
data_stream_id = None
stream_host_id = None
stream_host_collection_id = None
ds_server_url = None
events_processed_count = 0
stream_object_event_count = 0

# Neo4j settings
neo4j_uri = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
neo4j_user = os.getenv("NEO4J_USER", "neo4j")
neo4j_password = os.getenv("NEO4J_PASSWORD", "Pass@word")

# Initialize Neo4j driver
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))


def on_create(data: dict) -> dict | None:
    return {}


def on_receive(data: dict) -> dict | None:

    result = update_node_graph('/app/logs')
    print(result)
    return result


def on_destroy() -> dict | None:
    return {}



# def _update_neo4j_node_graph(events: dict):
#     for key, event in events.items():
        
#         if(event['stream_object_id'] is None):
#             continue
        
#         with driver.session() as session:
#             session.write_transaction(_merge_stream_object, event)
            
            
#             # print(f"\nStream Object: {key}")
#         #     print(f"  Count: {event['count']}")
#         #     print(f"  Last Updated: {event['last_updated']}")
#         #     print(f"  Data Stream ID: {event['data_stream_id']}")
#         #     print(f"  Data Stream Name: {event['data_stream_name']}")
#         #     print(f"  Stream Object ID: {event['stream_object_id']}")
#         #     print(f"  Stream Object Name: {event['stream_object_name']}")
#         #     print(f"  Stream Object Type: {event['stream_object_type']}")
#         #     print(f"  SH ID: {event['sh_id']}")
#         #     print(f"  SH Name: {event['sh_name']}")
#         #     print(f"  SH Collection ID: {event['sh_collection_id']}")
        


# def _merge_stream_object(tx, event):
#     query = """
#     MERGE (so:StreamObject {id: $so_id})
#     SET so.title = $so_title,
#         so.type = $so_type,
#         so.event_count = $so_event_count,
#         so.last_updated = $last_updated
#     """

#     tx.run(query, {
#         "so_id": event['stream_object_id'],
#         "so_title": event['stream_object_name'],
#         "so_type": event['stream_object_type'],
#         "so_event_count": event['count'],
#         "last_updated": datetime.now().isoformat()
#     })


# def _merge_stream_object_edge(tx):
#     query = """
#         MATCH (so:StreamObject {id: $so_id})
    
#         MERGE (sot:StreamObject {id: $so_target_id})
#         SET sot.last_updated = $last_updated
        
#         WITH so, sot
    
#         MERGE (so)-[r:CONNECTS_TO {
#                 id: $sh_rel_id, 
#                 source_id: $so_id, 
#                 target_id: $so_target_id,
#                 last_updated: $last_updated
#             }]->(sot)
#     """

#     tx.run(query, {
#         "so_id": stream_object_id,
#         "so_target_id": stream_object_target_id,
#         "sh_rel_id": stream_object_id + "_" + stream_object_target_id,
#         "last_updated": datetime.now().isoformat()
#     })


# def _merge_sh_and_so_edge(tx):
#     query = """
#         MATCH (so:StreamObject {id: $so_id})
    
#         MERGE (sh:StreamHost {id: $sh_id})
#         SET sh.title = $sh_title,
#             sh.last_updated = $last_updated

#         WITH so, sh

#         MERGE (sh)-[shr:EXECUTED { 
#                 id: $sh_rel_id, 
#                 source_id: $sh_id,
#                 target_id: $so_id,
#                 last_updated: $last_updated
#             }]->(so)
#     """

#     tx.run(query, {
#         "so_id": stream_object_id,
#         "sh_rel_id": stream_host_id + "_" + stream_object_id,
#         "sh_id": stream_host_id,
#         "sh_title": stream_host_title,
#         "last_updated": datetime.now().isoformat()
#     })


# def _merge_sh_collection_and_sh_edge(tx):
#     query = """
#         MATCH (sh:StreamHost {id: $sh_id})
    
#         MERGE (c:Collection {id: $sh_collection_id})
#         SET c.title = $sh_collection_title,
#             c.last_updated = $last_updated

#         WITH sh, c
        
#         MERGE (c)-[cr:BELONGS_TO { 
#                 id: $sh_collection_rel_id
#             }]->(sh)
#         ON CREATE SET cr.source_id = $sh_collection_id, 
#             cr.target_id = $sh_id,
#             cr.last_updated = $last_updated
#     """

#     tx.run(query, {
#         "sh_id": stream_host_id,
#         "sh_collection_id": stream_host_collection_id,
#         "sh_collection_title": stream_host_collection_title,
#         "sh_collection_rel_id": stream_host_collection_id + "_" + stream_host_id,
#         "last_updated": datetime.now().isoformat()
#     })


# def _merge_ds_and_sh_collection_edge(tx):
#     query = """
#         MATCH (c:Collection {id: $sh_collection_id})
    
#         MERGE (ds:DataStream {id: $ds_id})
#         SET ds.title = $ds_title,
#             ds.last_updated = $last_updated
        
#         WITH c, ds
        
#         MERGE (ds)-[dsr:BELONGS_TO { 
#                 id: $ds_rel_id
#             }]->(c)
#         ON CREATE SET dsr.source_id = $ds_id, 
#             dsr.target_id = $sh_collection_id,
#             dsr.last_updated = $last_updated
#     """

#     tx.run(query, {
#         "sh_collection_id": stream_host_collection_id,
#         "ds_id": data_stream_id,
#         "ds_title": data_stream_title,
#         "ds_rel_id": data_stream_id + "_" + stream_host_collection_id,
#         "last_updated": datetime.now().isoformat()
#     })


# def _merge_node_event_count(tx):
#     query = """
#     MERGE (so:StreamObject {id: $so_id})
#     SET so.event_count = $so_event_count,
#         so.last_updated = $last_updated
#     """

#     tx.run(query, {
#         "so_id": stream_object_id,
#         "so_event_count": stream_object_event_count,
#         "last_updated": datetime.now().isoformat()
#     })