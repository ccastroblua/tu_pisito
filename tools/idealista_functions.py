import base64
import requests
import json
import dotenv
import os
import pandas as pd
from config.configuration import engine
from datetime import datetime

dotenv.load_dotenv()

# Get current time:
now = datetime.now()
current_time = now.strftime("%d-%m-%y-%Hh%Mm%Ss")


def get_idealista_token():
    """Getting idealista token to perform API requests.

    Returns:
        Dictionary: Dictionary with API idealista token.
    """
    # Getting idealista pass from .env:
    idealista_pass = os.getenv("idealista")

    # Let's start getting requests from idealista API:
    # First, let's get the token:
    url_idealista_token = "https://api.idealista.com/oauth/token"

    # Coding into base 64 our credentials:
    auth = "Basic " + base64.b64encode(idealista_pass.encode("ascii")).decode("ascii")

    # Parameters to get the API credentials:
    headers = {"Authorization" : auth,
                "Content-Type" : "application/x-www-form-urlencoded;charset=UTF-8"}
    params = {"grant_type" : "client_credentials",
                "scope" : "read"}

    # We do the request:
    response = requests.post(url_idealista_token, 
                            headers = headers, 
                            params = params)

    # We get the final token:
    bearer_token = json.loads(response.text)["access_token"]

    return bearer_token


# Now i make a request to the API for some results:

# Function to call idealista API and get a request:
def idealista_request(bearer_token, lat_lon, distance=2000):
    """Requesting all apartments from idealista API, giving them latitude and logitude within 2000 meters distance from that coordinates.

    Args:
        bearer_token (Dictionary): Dictionary with token and parameters to perform request.
        lat_lon (string): latitude and longitude with format "{latitude},{longitude}".
        distance (int, optional): [description]. Defaults to 2000.

    Returns:
        Dictionary: Dictionary with all the information from the apartments from idealista API request.
    """    
    url = "https://api.idealista.com/3.5/es/search"

    headers = {'Content-Type': 'Content-Type: multipart/form-data;', 
               'Authorization' : 'Bearer ' + bearer_token}

    parameters = {"propertyType": "homes",
                  "center": lat_lon,
                  "operation": "sale",
                 "distance": distance}

    content = requests.post(url, headers = headers, params = parameters)
    result = json.loads(content.text)

    return result

# Let's define some dictionaries:

need_renewal = {
    "good": 0,
    "renew": 1,
    "newdevelopment": 0
}

house_types = {
    "flat": 0,
    "penthouse": 2,
    "duplex": 1,
    "house": 3,
    "chalet": 3
}

neighborhoods_names = {
    "Malasa??a-Universidad": "Malasa??a-Universidad",
    "Villaverde Alto": "San Andr??s"
}

districts_names = {
    "Centro": "Centro",
    "Arganzuela": "Arganzuela",
    "Retiro": "Retiro",
    "Barrio de Salamanca": "Salamanca",
    "Chamart??n": "Chamart??n",
    "Tetu??n": "Tetu??n",
    "Chamber??": "Chamber??",
    "Fuencarral": "Fuencarral",
    "Moncloa": "Moncloa",
    "Latina": "Latina",
    "Carabanchel": "Carabanchel",
    "Usera": "Usera",
    "Puente de Vallecas": "Puente de Vallecas",
    "Moratalaz": "Moratalaz",
    "Ciudad Lineal": "Ciudad Lineal",
    "Hortaleza": "Hortaleza",
    "Villaverde": "Villaverde",
    "Villa de Vallecas": "Villa de Vallecas",
    "Vic??lvaro": "Vicalvaro",
    "San Blas": "San Blas",
    "Barajas": "Barajas"
}


def transform_idealista(result, index):
    """Transform 1 idealista request result into 2 dictionary for importing into MySQL DB and predicting apartments prices.

    Args:
        result (DataFrame): DataFrame from the result of idealista API request.
        index (int): Index from the apartment we want to clean.

    Returns:
        dic_mysql (Dictionary): Dictionary to append in a list in order to import into MySQL DB.
        dic_prediction (Dictionary): Dictionary to append in a list in order to predict the price of apartments. 
    """    
    # First, we transform easy information:

    name = result["elementList"][index]["suggestedTexts"]["title"]
    sq_mt_built = result["elementList"][index]["size"]
    n_rooms = result["elementList"][index]["rooms"]
    n_bathrooms = result["elementList"][index]["bathrooms"]
    latitude = result["elementList"][index]["latitude"]
    longitude = result["elementList"][index]["longitude"]
    address = result["elementList"][index]["address"]
    buy_price = result["elementList"][index]["price"]
    url = result["elementList"][index]["url"]

    try:
        floor = float(result["elementList"][index]["floor"])
    except: 
        floor = 0

    # Now, let's move on to manipulate "true" and "false" information and change it to binary:

    try:
        is_new_development = int(result["elementList"][index]["newDevelopment"])
    except:
        is_new_development = 0

    try:
        has_lift = int(result["elementList"][index]["hasLift"])
    except:
        has_lift = 0

    try:
        is_exterior = int(result["elementList"][index]["exterior"])
    except:
        is_exterior = 0

    try:
        has_parking = int(result["elementList"][index]["parkingSpace"]["isParkingSpaceIncludedInPrice"])
    except:
        has_parking = 0


    # Let's change variable that need some dictionaries:

    is_renewal_needed = need_renewal.get(result["elementList"][index]["status"])
    house_type_id = house_types.get(result["elementList"][index]["propertyType"])


    # And finally with some queries:
    
    # Transforming neighborhood data:
    neighborhood = neighborhoods_names.get(result["elementList"][index]["neighborhood"])
    
    if neighborhood == None:
        neighborhood = result["elementList"][index]["neighborhood"]
    
    neighborhood_df = pd.read_sql_query(
    f"""
    SELECT neighborhood_id
    FROM neighborhoods
    WHERE neighborhood_name = "{neighborhood}";
    """, engine)

    neighborhood_id = int(neighborhood_df["neighborhood_id"][0])
    
    # Transforming district data:
    district = districts_names.get(result["elementList"][index]["district"])
    
    district_df = pd.read_sql_query(
    f"""
    SELECT district_id
    FROM districts
    WHERE district_name = "{district}";
    """, engine)
    
    district_id = int(district_df["district_id"][0])
    
    # Getting value_m2 column:
    value_m2_df = pd.read_sql_query(
    f"""
    SELECT value_m2
    FROM neighborhoods
    WHERE neighborhood_name = "{neighborhood}";
    """, engine)
    
    value_m2 = float(value_m2_df["value_m2"][0])    
    
    
    # We make two dictionaries: one for uplaoding dataset to mysql and another one for predictions:
    dic_mysql = {
                        "sq_mt_built": sq_mt_built,
                        "n_rooms": n_rooms,
                        "n_bathrooms": n_bathrooms,
                        "latitude": latitude,
                        "longitude": longitude,
                        "address": address,
                        "buy_price": buy_price,
                        "is_new_development": is_new_development,
                        "is_renewal_needed": is_renewal_needed,
                        "has_lift": has_lift,
                        "is_exterior": is_exterior,
                        "has_parking": has_parking,
                        "floor": floor,
                        "neighborhood_id": neighborhood_id,
                        "house_type_id": house_type_id,
                        "district_id": district_id
    }
    
    dic_prediction = {
                        "name": name,
                        "sq_mt_built": sq_mt_built,
                        "n_rooms": n_rooms,
                        "n_bathrooms": n_bathrooms,
                        "latitude": latitude,
                        "longitude": longitude,
                        "buy_price": buy_price,
                        "is_new_development": is_new_development,
                        "is_renewal_needed": is_renewal_needed,
                        "has_lift": has_lift,
                        "is_exterior": is_exterior,
                        "has_parking": has_parking,
                        "floor": floor,
                        "house_type_id": house_type_id,
                        "value_m2": value_m2,
                        "neighborhood": neighborhood,
                        "district": district,
                        "url": url
    }
    
    return dic_mysql, dic_prediction

# Now, i define a function to transform both dictionaries in dataframes:
def creating_dataframe(result):
    """Function that creates from a whole result of idealista API two DataFrames one for importing into MySQL DB and one for predicting apartments prices.

    Args:
        result (DataFrame): DataFrame from the result of idealista API request.

    Returns:
        DataFrame: DataFrame ready to import into MySQL DB.
        DataFrame: DataFrame ready to predict the price of apartments. 
    """    
    new_list1 = []
    new_list2 = []
    
    for i in range(len(result["elementList"])):
        if "neighborhood" in result["elementList"][i].keys():
            dic1, dic2 = transform_idealista(result, i)
            new_list1.append(dic1)
            new_list2.append(dic2)
        
    return pd.DataFrame(new_list1), pd.DataFrame(new_list2)


# And make a function to import idealista dataframe to mysql:
def import_idealista_to_mysql(df):
    """Function to import a DataFrame into apartments table MySQL DB.

    Args:
        df (DataFrame): DataFrame ready to import into MySQL DB.

    Returns:
        None
    """    
    for i, row in df.iterrows():

        # Loading the row to MySQL
        engine.execute(f"""
        INSERT apartments (sq_mt_built,
                            n_rooms,
                            n_bathrooms,
                            latitude,
                            longitude,
                            address,
                            buy_price,
                            is_new_development,
                            is_renewal_needed,
                            has_lift,
                            is_exterior,
                            has_parking,
                            floor,
                            neighborhood_id,
                            house_type_id,
                            district_id ) VALUES
        ({row["sq_mt_built"]},
        {row["n_rooms"]},
        {row["n_bathrooms"]},
        {row["latitude"]},
        {row["longitude"]},
        "{row["address"]}",
        {row["buy_price"]},
        {row["is_new_development"]},
        {row["is_renewal_needed"]},
        {row["has_lift"]},
        {row["is_exterior"]},
        {row["has_parking"]},
        {row["floor"]},
        {row["neighborhood_id"]},
        {row["house_type_id"]},
        {row["district_id"]});
        """)
        
    print("Dataframe cargado en MySQL!")


#Transforming latitude and longitude to lat,lon for idealista API:
def transform_lat_lon(latitude, longitude):
    """Transforming latitude and longitude in a format idealista API can use.

    Args:
        latitude (int): Latitude from a place.
        longitude (int): Longitude from a place.

    Returns:
        string: Latitude and longitude combined in "{latitude},{longitude}".
    """    
    lat_lon = str(latitude) + "," + str(longitude)
    return lat_lon


#Let's get the whole process in one functions:
def pipeline_idealista(lat_lon):
    """Complex function that calls other functions working with Idealista API. The objective of this function is simplify in one function API request and DataFrame transformation.
    - It makes idealista API request for a token.
    - It makes idealista API request for apartments near a coordinates.
    - Create 2 DataFrame for importing in MySQL DB and for ML model.
    - Finally, create 2 CSV with those DataFrame to save that information.

    Args:
        lat_lon (string): latitude and longitude in "{latitude},{longitude}" format.

    Returns:
        DataFrame: DataFrame ready to use it to predict apartments prices.
    """    
    token = get_idealista_token()
    result = idealista_request(token, lat_lon)
    df_mysql, df_pred = creating_dataframe(result)
    # import_idealista_to_mysql(df_mysql)
    df_mysql.to_csv(f"./data/real_data/df_mysql_{current_time}.csv", index = False)
    df_pred.to_csv(f"./data/real_data/df_pred_{current_time}.csv", index = False)
    return df_pred