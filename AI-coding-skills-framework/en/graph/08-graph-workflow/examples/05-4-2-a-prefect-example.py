# pip install prefect

from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner

@task(retries=3, retry_delay_seconds=10)
def extract_task(documents: list) -> dict:
    print(f"Extracting from {len(documents)} docs...")
    # entities = extract_entities_batch(documents)
    return {"entities": [], "relations": []}

@task
def dedup_task(data: dict) -> dict:
    print("Deduplicating...")
    # canonical, mapping = deduplicate_entities(data["entities"])
    return data

@task
def validate_task(data: dict) -> dict:
    print("Validating against the ontology...")
    return data

@task
def load_task(data: dict) -> dict:
    print(f"Loading {len(data['entities'])} entities into Neo4j...")
    return {"loaded": len(data["entities"])}

@flow(name="graph-etl", task_runner=ConcurrentTaskRunner())
def graph_etl_flow(documents: list):
    extracted = extract_task(documents)
    deduped = dedup_task(extracted)
    validated = validate_task(deduped)
    result = load_task(validated)
    return result

# Run
# graph_etl_flow(["Doc 1", "Doc 2", "Doc 3"])

# Schedule: run hourly
# from prefect.deployments import Deployment
# Deployment.build_from_flow(
#     flow=graph_etl_flow,
#     name="hourly-graph-etl",
#     schedule={"cron": "0 * * * *"},
# )
