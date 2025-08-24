CREATE USER auth_service_user WITH ENCRYPTED PASSWORD 'plainpassword';
CREATE DATABASE auth OWNER auth_service_user;

CREATE USER conversion_service_user WITH ENCRYPTED PASSWORD 'plainpassword';
CREATE DATABASE conversion OWNER conversion_service_user;