import folium
import streamlit as st

from streamlit_folium import st_folium

'''
# Building AI front
'''

st.markdown('''
  markdown
''')

#48.859932, 2.343623 paris centre

# center on Liberty Bell, add marker
m = folium.Map(location=[48.859932, 2.343623], zoom_start=12)


# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)


#url = 'https://taxifare.lewagon.ai/predict'

#if url == 'https://taxifare.lewagon.ai/predict':

#    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')
