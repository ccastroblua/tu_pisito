import streamlit as st
from PIL import Image
from tools import functions as func
from tools import google_functions as g_func
from tools import idealista_functions as i_func



st.write("""
# Get your apartment in Madrid with the best price in the market!

""")

"With this app you will get the prices from apartments in an specific neighborhood that you want or near an specific address."

# st.text(""" TEST """)

imagen = Image.open("images/madrid.jpg")
st.image(imagen, use_column_width=True)

st.subheader("Please provide a neighborhood for your next apartment in the sidebar.")

nh_df = func.get_neighborhoods()

option = st.sidebar.selectbox(
    "In which neighborhood do you want to live?", nh_df["neighborhood_name"]
)

"You selected:", option

df_lat_lon = func.get_coordinates_neighborhood(option)

"Latitude:", df_lat_lon["latitude"][0]
"longitude:", df_lat_lon["longitude"][0]

# Preparing lat_lon variable to use with Idealista API:
lat_lon = str(df_lat_lon["latitude"][0]) + "," + str(df_lat_lon["longitude"][0])

df_user_inputs = func.user_input_features()

df_user_inputs