from config.configuration import engine
import pandas as pd
import numpy as np
import h2o
from h2o.automl import H2OAutoML


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


