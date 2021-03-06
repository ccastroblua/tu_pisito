from config.configuration import engine
import dotenv
import os
import requests

dotenv.load_dotenv()
gm_key = os.getenv("google_maps")


# Function to send an specific request to Google Maps API:
def get_places(lat, lon, radius=1000, keyword = "", type_ = ""):
    """It gets a response from Google API with a max of 20 results to a determined request with
    keywords, type of place, longitude, latitude and radius.

    Parameters:
    lat (float): Latitude.
    lon (float): Longitude.
    radius (float): Radius of the search near by.
    keyword (str): To search for afinity. Can be many words.
    type_ (str): Different type of places to search ("restaurants", etc). Has to be only one word.
    
    Returns: 
    list: list of diccionaries (JSON format) with a maximum of 20 places that fullfil asked conditions 
    """
    
    url_nearby_search = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    loc = str(lat) + "," + str(lon)
    
    parameters = {"key": gm_key, "location": loc, "radius": radius, "keyword": keyword, "type": type_}
    
    response = requests.get(
    url=url_nearby_search, 
    params = parameters
    )
    
    data = response.json()
    
    return data


# This function add up the information of a Google Maps API request to a list in order to graphic that information with folium
def google_places(response, place_type, places_list=[]):
    """It adds name, place type, latitude and longitude to a current list with a specific response from Google Maps API.
    
    Parameters:
    response (dic): dicctionaries with a response from Google Maps API.
    place_type (str): type of place
    place_list (list): current list where we will add some more row of data

    Returns: 
    list: list of diccionaries (JSON format) with name of the place, latitude, longitude,
    and a column for each condition.
    """
    for result in response["results"]:
        name = result["name"]
        place_type = place_type
        latitude = result["geometry"]["location"]["lat"]
        longitude = result["geometry"]["location"]["lng"]

        dicc = {
            "name": name, 
            "place_type": place_type, 
            "latitude": latitude, 
            "longitude": longitude
        }

        places_list.append(dicc)

    return places_list