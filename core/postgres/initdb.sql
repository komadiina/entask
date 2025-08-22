CREATE USER auth_service_user WITH ENCRYPTED PASSWORD 'plainpassword';
CREATE DATABASE auth OWNER auth_service_user;