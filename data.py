
import os
import pandas as pd
import numpy as np
from google.cloud import bigquery

from shapely.geometry import MultiPolygon,Point,Polygon
from shapely.wkt import loads
from shapely.ops import unary_union
#from shapely.errors  import GEOSException

from shapely import wkt, ops
from pyproj import Transformer
from tqdm import tqdm




def get_list_building_df(code_insee: str) -> pd.DataFrame:
    """
    Get a dataframe for a specific building from BQ.
    """
    table_name = get_full_table_name()
    query = f"""
        SELECT geom_groupe,batiment_groupe_id,classe_bilan_dpe
        FROM {table_name}
        WHERE batiment_groupe_id like '{code_insee}%'

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


def convert_prof_geo(polygone_prog) : #polygone geo
  transformer = Transformer.from_crs("epsg:2154", "epsg:4326", always_xy=True)
  batiments = polygone_prog
  newbat = ops.transform(transformer.transform, batiments)
  return newbat


def add_geom_groupe_geo_and_convert_geom_groupe (newdf=None) -> pd.DataFrame:

    batiment = newdf['geom_groupe']
    newbat_prof=[]
    newbat_geo = []
    transformer = Transformer.from_crs("epsg:2154", "epsg:4326", always_xy=True)
    for i in range(len(batiment)) :
        newbat_prof.append(loads(batiment[i]))
        newbat_geo.append(ops.transform(transformer.transform, newbat_prof[i]))

    newdf['geom_groupe'] = newbat_prof
    newdf['geom_groupe_geo']=newbat_geo

    return newdf


def prepare_df(code_insee: str) -> pd.DataFrame:
    df = get_list_building_df('75111')
    df_with_geo = add_geom_groupe_geo_and_convert_geom_groupe(df)

    return df_with_geo

if __name__ == "__main__":
    print('on est dans le main')
    df = (prepare_df('75111'))
    print(df.head())
