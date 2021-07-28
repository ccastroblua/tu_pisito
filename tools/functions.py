from re import sub
from config.configuration import engine
import pandas as pd
import numpy as np
import h2o
from h2o.automl import H2OAutoML
from geopy.geocoders import Nominatim
import streamlit as st
from functions import google_functions as g_func


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

    data = {"bar": bar,
            "restaurant": restaurant,
            "cafe": cafe,
            "subway_station": subway_station,
            "train_station": train_station,
            "supermarket": supermarket,
            "gym": gym,
            "park": park,
            "primary_school": primary_school,
            "secondary_School": secondary_school,
            "shopping_mall": shopping_mall
            }

    return pd.DataFrame(data, index=[0])