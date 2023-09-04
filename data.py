
import os
import pandas as pd
import numpy as np
from google.cloud import bigquery



def get_building_df(building_id: str) -> pd.DataFrame:
    """
    Get a dataframe for a specific building from BQ.
    """
    table_name = get_full_table_name()
    query = f"""
        SELECT *
        FROM {table_name}
        WHERE batiment_groupe_id = '{building_id}'
        LIMIT 1
    """
    client = bigquery.Client(project=os.environ["GCP_PROJECT"])
    query_job = client.query(query)
    result = query_job.result()
    return result.to_dataframe()


def get_full_table_name() -> str:
    """
    Get the name of the BQ table.
    """
    gcp_project = os.environ.get("GCP_PROJECT")
    bq_dataset = os.environ.get("BQ_DATASET")
    table = os.environ.get("BQ_RAW_DATA")
    return f"{gcp_project}.{bq_dataset}.{table}"
