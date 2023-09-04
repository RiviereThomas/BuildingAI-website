import folium
import streamlit as st
from  data import  get_list_building_df,prepare_df
from streamlit_folium import st_folium
from ipyleaflet import Map, GeoJSON
import geopandas as gpd
import ipywidgets as widgets
from IPython.display import display


import ipywidgets as widgets
from IPython.display import display

from shapely.geometry import MultiPolygon,Point,Polygon
from shapely.wkt import loads
from shapely.ops import unary_union


from shapely import wkt, ops
from pyproj import Transformer
from tqdm import tqdm

@st.cache_data
def load_data():
    # Chargez votre DataFrame ici
    # Par exemple, si vous chargez à partir d'un fichier CSV :
    df = prepare_df('75111')
    return df


@st.cache(allow_output_mutation=True)
def create_interactive_map(df):
    # Créez une carte Folium
    center =[48.863218, 2.377144]
    m = folium.Map(location=center, zoom_start=14, zoom_control=False)  # Coordonnées du centre de la carte


    # Ajoutez les polygones géographiques à la carte
    for index, row in df.iterrows():
         geojson = row['geom_groupe_geo']  # Assurez-vous que votre DataFrame a une colonne 'geometry' avec des données GeoJSON ou WKT
         folium.GeoJson(geojson).add_to(m)
    return m

# Appelez la fonction pour charger le DataFrame (elle sera mise en cache) puis charger la maps
data = load_data().head(20)
interactive_map = create_interactive_map(data)


'''
# Building AI front
'''




# Affichez la carte dans Streamlit
st.markdown("## Carte des Polygones Géographiques")

# call to render Folium map in Streamlit
st_folium(interactive_map, width=725)
#st.write(interactive_map, width=725)
