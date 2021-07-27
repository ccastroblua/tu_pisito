USE tu_pisito;

SELECT *
FROM districts;

SELECT *
FROM house_types;

SELECT *
FROM neighborhoods;

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
WHERE neighborhood_name = "Malasaña-Universidad"