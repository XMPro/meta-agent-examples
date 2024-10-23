# TODO include example of this
from src.packages.logs_to_node_graph.action_agent.source_code.logs_to_neo4j import update_node_graph
from datetime import time

def on_create(data: dict) -> dict | None:
    # update_frequency_in_seconds = data.get('update_frequency_in_seconds', 60)

    # while True:
    #     events = update_node_graph('/app/logs')
    #     print(events)
    #     time.sleep(update_frequency_in_seconds)
    return {}


def on_receive(data: dict) -> dict | None:
    events = update_node_graph('/app/logs')
    return events


def on_destroy() -> dict | None:
    return {}
