USE tu_pisito;

SELECT *
FROM districts;

SELECT *
FROM house_types;

SELECT *
FROM neighborhoods
ORDER BY district_id ASC;

SELECT neighborhood_id
FROM neighborhoods
WHERE neighborhood_name = "Los Ángeles";

SELECT district_id
FROM districts
WHERE district_name = "Villaverde";

SELECT *
FROM apartments
ORDER BY apartment_id DESC;

DELETE FROM apartments
WHERE apartment_id = 9131;

SELECT *
FROM neighborhoods
WHERE neighborhood_name = "Malasaña-Universidad";

SELECT value_m2
FROM neighborhoods
WHERE neighborhood_name = "Malasaña-Universidad";

SELECT neighborhood_name, latitude, longitude, districts.district_id, district_name
FROM neighborhoods
LEFT JOIN districts
ON neighborhoods.district_id = districts.district_id;

SELECT neighborhood_name, district_name, districts.district_id, latitude, longitude
FROM neighborhoods
LEFT JOIN districts
ON neighborhoods.district_id = districts.district_id;

SELECT district_id, district_name
FROM districts
ORDER BY district_id ASC;

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

SELECT neighborhood_name
FROM neighborhoods
ORDER BY neighborhood_id ASC;

SELECT latitude, longitude
FROM neighborhoods
WHERE neighborhood_name = "Guindalera";