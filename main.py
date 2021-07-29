import streamlit as st
from PIL import Image
from tools import functions as func
from tools import google_functions as g_func
from tools import idealista_functions as i_func
import pandas as pd


st.write("""
# Get your apartment in Madrid with the best price in the market!

""")

"With this app you will get the prices from apartments in an specific neighborhood that you want or near an specific address."

# st.text(""" TEST """)

imagen = Image.open("images/madrid.jpg")
st.image(imagen, use_column_width=True)

st.subheader("Please select how do you want to search your next apartment in the sidebar:")



# Initial sidebar option how you going to search for apartments:
df_option = [
    "Choose an option",
    "Search in a neighborhood",
    "Search with an address"
    ]

initial_selection = st.sidebar.selectbox(
    "How do you want to search for your apartment?", df_option
)

"You selected search is:", initial_selection

if initial_selection == "Search in a neighborhood":

    # Get apartments through neighborhood coordinates:
    nh_df = func.get_neighborhoods()

    option = st.sidebar.selectbox(
        "In which neighborhood do you want to live?", nh_df["neighborhood_name"]
    )

    "You selected ", option, "neighborhood."

    df_lat_lon = func.get_coordinates_neighborhood(option)

    latitude = df_lat_lon["latitude"][0]
    longitude = df_lat_lon["longitude"][0]

    lat_lon = i_func.transform_lat_lon(df_lat_lon["latitude"][0], df_lat_lon["longitude"][0])

    df_user_inputs = func.user_input_features()

elif initial_selection == "Search with an address":

    # Get apartments through address option:
    address = st.sidebar.text_input("Please provide an address in Madrid to search for your aparment:")
    
    if address != "":
        "Your searching address is ", address, ""
    
    coord_address = func.get_coordinates(address)
    
    latitude = coord_address["latitude"]
    longitude = coord_address["longitude"]

    lat_lon = i_func.transform_lat_lon(coord_address["latitude"], coord_address["longitude"])

    df_user_inputs = func.user_input_features()





st.sidebar.subheader("Confirm your selections:")

confirmation = st.sidebar.checkbox("Let's search for my apartment!")

if confirmation:
    if initial_selection == df_option[1] or initial_selection == df_option[2]:

        # apartments_df = pd.read_csv("./data/real_data/test.csv")
        apartments_df = i_func.pipeline_idealista(lat_lon)
        
        predicted_df = func.predict_prices(apartments_df)
        columns = ["name",
                "sq_mt_built",
                "n_rooms",
                "n_bathrooms",
                "floor",
                "buy_price",
                "neighborhood",
                "url"
        ]
        show_df = predicted_df[columns]
        st.table(show_df)


        apartments_list = list(range(len(apartments_df.index)))


        apartments_option = st.selectbox(
        "Which apartment do you like? (Select the apartment number of the table above)", ["Choose one"] + apartments_list
        )

        if apartments_option != "Choose one":
            
            st.subheader("Your selected apartments has:")
            predicted_df.loc[apartments_option].astype(str)["sq_mt_built"], "square meters."
            predicted_df.loc[apartments_option].astype(str)["n_rooms"], "rooms."
            predicted_df.loc[apartments_option].astype(str)["n_bathrooms"], "bathrooms."
            "It's on the ", predicted_df.loc[apartments_option].astype(str)["floor"], " floor."
            "It's in ", predicted_df.loc[apartments_option].astype(str)["neighborhood"], " neighborhood."

            if int(predicted_df.loc[apartments_option].astype(str)["is_new_development"]) == 1:
                "It's brand new!"
            if int(predicted_df.loc[apartments_option].astype(str)["is_renewal_needed"]) == 1:
                "Needs a renewal."
            if int(predicted_df.loc[apartments_option].astype(str)["has_lift"]) == 1:
                "Has lift."
            if int(predicted_df.loc[apartments_option].astype(str)["has_parking"]) == 1:
                "It has parking for your car."

            "URL to see the aparment: ", predicted_df.loc[apartments_option].astype(str)["url"]

            buy_prediction = int(predicted_df.loc[apartments_option].astype(str)["buy_prediction"])
            buy_price = int(predicted_df.loc[apartments_option].astype(str)["buy_price"])
            "Buying price: ", buy_price
            "Predicted value: ", buy_prediction

            good = func.is_good_purchase(buy_price, buy_prediction)
            if good:
                st.write(""" ### THIS IS A GREAT OFFER!""")

            ap_latitude = apartments_df.loc[apartments_option]["latitude"].astype(str)
            ap_longitude = apartments_df.loc[apartments_option]["longitude"].astype(str)

        st.subheader("Now you can see how life in this property looks like:")
        lifestyle_option = st.checkbox("Show me my new home lifestyle:")
        if lifestyle_option:
            try:
                df_google = func.get_google_data(df_user_inputs, ap_latitude, ap_longitude)
                df_google.loc[-1] = ["This is your new apartment", "apartment", ap_latitude, ap_longitude]
                df_google.index += 1
                df_google = df_google.sort_index()
                func.maps(df_google, ap_latitude, ap_longitude)
            except:
                "Please select any lifestyle options from the sidebar!"


