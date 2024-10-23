# TODO include example of this
from src.packages.logs_to_node_graph.action_agent.source_code.logs_to_neo4j import update_node_graph

def on_create(data: dict) -> dict | None:
    return {}


def on_receive(data: dict) -> dict | None:
    # TODO split this up into separate files
    events = update_node_graph('/app/logs')
    return events


def on_destroy() -> dict | None:
    return {}
