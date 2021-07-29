from config.configuration import engine
import pandas as pd
import numpy as np
import h2o
from h2o.automl import H2OAutoML
from geopy.geocoders import Nominatim
import streamlit as st
import google_functions as g_func
from folium import Choropleth, Circle, Marker, Icon, Map
import folium
from streamlit_folium import folium_static


def getting_mysql_data(dropping_price=True):

    # Querying database for all our data:
    mysql_df = pd.read_sql_query(
    f"""
    SELECT sq_mt_built, 
            n_rooms, 
            n_bathrooms, 
            apartments.latitude, 
            apartments.longitude, 
            is_new_development, 
            is_renewal_needed, 
            has_lift, 
            is_exterior, 
            has_parking, 
            floor, 
            house_type_id,
            value_m2,
            neighborhood_name,
            district_name,
            buy_price
    FROM apartments
    LEFT JOIN neighborhoods
    ON apartments.neighborhood_id = neighborhoods.neighborhood_id
    LEFT JOIN districts
    ON neighborhoods.district_id = districts.district_id
    ORDER BY apartment_id DESC;
    """, engine)

    # Renaming columns:
    mysql_df = mysql_df.rename(columns = {
    "neighborhood_name": "neighborhood",
    "district_name": "district"
       })

    # Changing price to log10 of price:

    mysql_df["log_buy_price"] = np.log10(mysql_df.buy_price)

    if dropping_price:
        mysql_df.drop("buy_price", axis=1, inplace=True)

    return mysql_df



def get_coordinates(address):
    geolocator = Nominatim(user_agent="tu_pisito")
    address += ", Madrid"
    try:
        location = geolocator.geocode(address)
        dic = {"latitude": location.latitude,
            "longitude": location.longitude
    }
    except:
        return "Please provide a correct address from Madrid."

    return dic


def get_neighborhoods():
    
    nh_df = pd.read_sql_query(
    f"""
    SELECT neighborhood_name
    FROM neighborhoods
    ORDER BY neighborhood_id ASC;
    """, engine)

    return nh_df


def get_coordinates_neighborhood(neighborhood):

    df = pd.read_sql_query(
    f"""
    SELECT latitude, longitude
    FROM neighborhoods
    WHERE neighborhood_name = "{neighborhood}";
    """, engine)

    return df


def user_input_features():
    """
    Function to save the info that the user give in the app
    Args: 
        non receive parameters
    Returns:
        A dataframe with the selections given by the user
    """
    lst = []

    bar = st.sidebar.checkbox("Do you need bars near?")
    restaurant = st.sidebar.checkbox("Do you need restaurants near?")
    cafe = st.sidebar.checkbox("Do you need cafes near?")
    subway_station = st.sidebar.checkbox("Do you need primary subway stations near?")
    train_station = st.sidebar.checkbox("Do you need primary train stations near?")
    supermarket = st.sidebar.checkbox("Do you need primary supermarkets?")
    gym = st.sidebar.checkbox("Do you need primary gyms near?")
    park = st.sidebar.checkbox("Do you need primary parks near?")
    primary_school = st.sidebar.checkbox("Do you need primary schools near?")
    secondary_school = st.sidebar.checkbox("Do you need secondary schools near?")
    shopping_mall = st.sidebar.checkbox("Do you need shopping malls near?")


    lst.append({"option": "bar",
            "confirmation": bar})
    lst.append({"option": "restaurant",
            "confirmation": restaurant})
    lst.append({"option": "cafe",
            "confirmation": cafe})
    lst.append({"option": "subway_station",
            "confirmation": subway_station})
    lst.append({"option": "train_station",
            "confirmation": train_station})
    lst.append({"option": "supermarket",
            "confirmation": supermarket})
    lst.append({"option": "gym",
            "confirmation": gym})
    lst.append({"option": "park",
            "confirmation": park})
    lst.append({"option": "primary_school",
            "confirmation": primary_school})
    lst.append({"option": "secondary_school",
            "confirmation": secondary_school})
    lst.append({"option": "shopping_mall",
            "confirmation": shopping_mall})

    return pd.DataFrame(lst)


def get_google_data(df, latitude, longitude):
    df = df[df["confirmation"]]
    lst = []

    for i, row in df.iterrows():
        data = g_func.get_places(latitude, longitude, radius=1000, type_ = row["option"])
        lst = g_func.google_places(data, row["option"], lst)

    return pd.DataFrame(lst)


def maps(df, initial_lat, initial_lon):
    """
    Function to create a folium map with the species presences
    Args: 
        df: dataframe
        initial_lat: latitude (float)
        initial_lon: longitude (float)
    Returns:
        A folium map
    """
    #showing the maps
    map_1 = folium.Map(tiles="OpenStreetMap", location=[initial_lat, initial_lon], zoom_start=15)

    for i,row in df.iterrows():
        
        place = {"location" : [row["latitude"],row["longitude"]],
                     "tooltip" : row["name"]}

        if row["place_type"] == "apartment":
            icon = Icon (
            color="blue",
            prefix="fa",
            icon="home",
            icon_color="black"
        )
        elif row["place_type"] == "supermarket":
            icon = Icon (
            color="orange",
            prefix="fa",
            icon="cart-arrow-down",
            icon_color="black"
        )
        elif row["place_type"] == "shopping_mall":
            icon = Icon (
            color="orange",
            prefix="fa",
            icon="shopping-bag",
            icon_color="black"
        )
        elif row["place_type"] == "cafe":
            icon = Icon (
            color="purple",
            prefix="fa",
            icon="coffee",
            icon_color="black"
        )
        elif row["place_type"] == "restaurant":
            icon = Icon (
            color="purple",
            prefix="fa",
            icon="cutlery",
            icon_color="black"
        )
        elif row["place_type"] == "primary_school":
            icon = Icon (
            color="darkred",
            prefix="fa",
            icon="graduation-cap",
            icon_color="black"
        )
        elif row["place_type"] == "bar":
            icon = Icon (
            color="purple",
            prefix="fa",
            icon="glass",
            icon_color="black"
        )
        elif row["place_type"] == "secondary_school":
            icon = Icon (
            color="darkred",
            prefix="fa",
            icon="graduation-cap",
            icon_color="black"
        )
        elif row["place_type"] == "subway_station":
            icon = Icon (
            color="red",
            prefix="fa",
            icon="subway",
            icon_color="black"
        )
        elif row["place_type"] == "train_station":
            icon = Icon (
            color="red",
            prefix="fa",
            icon="train",
            icon_color="black"
        )
        elif row["place_type"] == "gym":
            icon = Icon (
            color="black",
            prefix="fa",
            icon="futbol-o",
            icon_color="white"
        )
        else:
            icon = Icon (
            color="green",
            prefix="fa",
            icon="tree",
            icon_color="white"
        )

                

        marker = Marker(**place, icon = icon).add_to(map_1)

    return folium_static(map_1)


def predict_prices(df):
    h2o.init()
    saved_model = h2o.load_model("./models/GBM_grid__1_AutoML_20210728_185537_model_16")
    h2o_df = h2o.H2OFrame(df)
    predictions = saved_model.predict(h2o_df)
    h2o_df["prediction"] = predictions
    final_df = h2o_df.as_data_frame()
    final_df["buy_prediction"] = 10**final_df.prediction
    final_df = final_df.astype({"buy_prediction": int})
    # final_df.drop(cols, axis=1, inplace=True)
    return final_df