-- Generoitu käyttämällä Claude 3.5 Sonnet
-- create a .sql file that logs in as postgres user and creates a dabatase
-- named 'tehtävä4_jonne_vuorela' and then user that has priviledges edit tables in database.
-- integrate this script made with mysql workbench into that postgres {.sql scripti myslq workbenchista}

-- Create the database
CREATE DATABASE tehtava4_jonne_vuorela;

-- Create a user
CREATE USER app WITH PASSWORD 'pass';

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON DATABASE tehtava4_jonne_vuorela TO app;
