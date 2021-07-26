DROP DATABASE IF EXISTS tu_pisito;
CREATE DATABASE tu_pisito;

USE tu_pisito;

CREATE TABLE districts (
district_id INT PRIMARY KEY AUTO_INCREMENT,
district_name VARCHAR(100) NOT NULL
);

CREATE TABLE neighborhoods (
neighborhood_id INT PRIMARY KEY AUTO_INCREMENT,
neighborhood_name VARCHAR(100) NOT NULL,
district_id INT NOT NULL,
value_m2 FLOAT NOT NULL,
latitude FLOAT NOT NULL,
longitude FLOAT NOT NULL,
FOREIGN KEY (district_id) REFERENCES districts (district_id) ON DELETE CASCADE
);

CREATE TABLE house_types (
house_type_id INT PRIMARY KEY,
house_type_name VARCHAR(50) NOT NULL
);

CREATE TABLE apartments (
apartment_id INT PRIMARY KEY AUTO_INCREMENT,
sq_mt_built FLOAT NOT NULL,
n_rooms INT NOT NULL,
n_bathrooms INT NOT NULL,  
latitude FLOAT NOT NULL,
longitude FLOAT NOT NULL,
address VARCHAR(100),
buy_price FLOAT NOT NULL,  
is_new_development INT NOT NULL,  
is_renewal_needed INT NOT NULL, 
has_lift INT NOT NULL, 
is_exterior INT NOT NULL, 
has_parking INT NOT NULL,  
floor FLOAT NOT NULL,
neighborhood_id INT NOT NULL,
house_type_id INT NOT NULL,
district_id INT NOT NULL,
FOREIGN KEY (neighborhood_id) REFERENCES neighborhoods (neighborhood_id) ON DELETE CASCADE,
FOREIGN KEY (district_id) REFERENCES districts (district_id) ON DELETE CASCADE,
FOREIGN KEY (house_type_id) REFERENCES house_types (house_type_id) ON DELETE CASCADE
);