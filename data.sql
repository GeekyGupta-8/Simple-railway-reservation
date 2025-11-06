use computer_project;


CREATE TABLE trains (
    train_name varchar(255) UNIQUE,
    destination varchar(255),
    train_status varchar(255),
    fare DECIMAL(5,2),
    seats int DEFAULT 100
);

SELECT train_name, seats FROM trains WHERE seats > 0;
    
INSERT INTO trains (train_name, destination, train_status, fare, seats) VALUES
("Vande Bharat Express", "Delhi", "On time", "100.00", "120"),
("Rajdhani Express", "Mumbai", "On time", "250.00", "100"),
("Shatabdi Express", "Varanasi", "On time", "300.00", "150"),
("Duronto Express", "Chennai", "Delayed", "320.00", "250");

DROP TABLE trains;
--Putting some values for trains
CREATE TABLE bookings (
    pnr BIGINT UNIQUE,
    username VARCHAR(50),
    phoneno BIGINT,
    train_name VARCHAR(50),
    destination VARCHAR(50),
    fare DECIMAL(5,2),
    booking_time TIME,
    booking_date DATE,
    boarding_date DATE
);

DROP TABLE bookings;

SELECT * FROM trains;
SELECT * FROM bookings;