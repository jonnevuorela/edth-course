-- Generoitu käyttämällä Claude 3.5 Sonnet
-- create a .sql file that logs in as postgres user and creates a dabatase
-- named 'tehtävä4_jonne_vuorela' and then user that has priviledges edit tables in database.
-- integrate this script made with mysql workbench into that postgres {.sql scripti myslq workbenchista}


-- Create the schema
CREATE SCHEMA IF NOT EXISTS public;

-- Set the search path
SET search_path TO public;

-- Create tables
-- -----------------------------------------------------
-- Table gender
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS gender (
    id SERIAL PRIMARY KEY,
    gender VARCHAR(45) NOT NULL
);

-- -----------------------------------------------------
-- Table education_level
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS education_level (
    id SERIAL PRIMARY KEY,
    level VARCHAR(255) NOT NULL
);

-- -----------------------------------------------------
-- Table job_title
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS job_title (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL
);

-- -----------------------------------------------------
-- Table employee
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS employee (
    id SERIAL PRIMARY KEY,
    salary FLOAT NOT NULL,
    age INTEGER NOT NULL,
    years_of_experience FLOAT NOT NULL,
    gender_id INTEGER NOT NULL,
    education_level_id INTEGER NOT NULL,
    job_title_id INTEGER NOT NULL,
    CONSTRAINT fk_employee_gender
        FOREIGN KEY (gender_id)
        REFERENCES gender (id)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    CONSTRAINT fk_employee_education_level
        FOREIGN KEY (education_level_id)
        REFERENCES education_level (id)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    CONSTRAINT fk_employee_job_title
        FOREIGN KEY (job_title_id)
        REFERENCES job_title (id)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
);

-- Create indexes
CREATE INDEX idx_employee_gender ON employee(gender_id);
CREATE INDEX idx_employee_education_level ON employee(education_level_id);
CREATE INDEX idx_employee_job_title ON employee(job_title_id);

-- Grant privileges
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO app;
GRANT ALL PRIVILEGES ON SCHEMA public TO app;

-- Make sure new tables will be accessible by the user
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
GRANT ALL PRIVILEGES ON TABLES TO app;

ALTER DEFAULT PRIVILEGES IN SCHEMA public 
GRANT ALL PRIVILEGES ON SEQUENCES TO app;
