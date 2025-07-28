-- Original suggestion from Justin
SELECT p.project_name, d.name as device_name, d.created_at
FROM projects p
JOIN project_devices pd on p.id = pd.project_id
JOIN devices d on pd.device_id = d.id
ORDER BY p.project_name

-- After designing the tables, I think that could be
-- simplified to query for listing devices by project
SELECT p.project_name, d.device_name, d.created_at
FROM device d
JOIN project p on d.project_id = p.project_id
ORDER BY p.project_name


-- delete tables if exist / kids first / parents last
-- DROP TABLE IF EXISTS app
-- DROP TABLE IF EXISTS model
-- DROP TABLE IF EXISTS device
-- DROP TABLE IF EXISTS project
-- DROP TABLE IF EXISTS collaborator
-- DROP TABLE IF EXISTS user
-- DROP TABLE IF EXISTS team


-- team table creation
CREATE TABLE IF NOT EXISTS team (
    team_id SERIAL,
    team_name VARCHAR(32) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT pk_team_id PRIMARY KEY (team_id)
);

-- user table creation
CREATE TABLE IF NOT EXISTS user (
    user_id SERIAL,
    team_id INT NOT NULL,
    login_name VARCHAR(32) UNIQUE NOT NULL,
    -- password_hash VARCHAR(32) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT pk_user_id PRIMARY KEY (user_id),
    CONSTRAINT fk_team_id FOREIGN KEY (team_id) REFERENCES team (team_id) ON DELETE CASCADE
);

-- collaborator table creation
-- CREATE TABLE IF NOT EXISTS collaborator (
--     team_id INT NOT NULL,
--     user_id INT NOT NULL,
--     CONSTRAINT pk_team_user_id PRIMARY KEY (team_id, user_id) REFERENCES team (team_id) REFERENCES user (user_id) MATCH FULL
-- );
-- if above doe snot work create a normal table with 2 foreign keys
CREATE TABLE IF NOT EXISTS collaborator (
    collaborator_id SERIAL
    team_id INT NOT NULL,
    user_id INT NOT NULL,
    CONSTRAINT pk_collaborator_id PRIMARY KEY (collaborator_id),
    CONSTRAINT fk_team_id PRIMARY KEY(team_id) REFERENCES team (team_id) ON DELETE CASCADE,
    CONSTRAINT fk_user_id PRIMARY KEY(user_id) REFERENCES user (user_id) ON DELETE CASCADE
);

-- project table creation
CREATE TABLE IF NOT EXISTS project (
    project_id SERIAL,
    team_id INT,
    project_name VARCHAR(32) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT pk_project_id PRIMARY KEY (project_id),
    CONSTRAINT fk_team_id PRIMARY KEY (team_id) REFERENCES team (team_id) ON DELETE SET NULL
);

-- device table creation
CREATE TABLE IF NOT EXISTS device (
    device_id SERIAL,
    project_id INT,
    device_name VARCHAR(32) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT pk_device_id PRIMARY KEY (device_id),
    CONSTRAINT fk_project_id FOREIGN KEY (project_id) REFERENCES project (project_id) ON DELETE SET NULL
);

-- model table creation
CREATE TABLE IF NOT EXISTS model (
    model_id SERIAL,
    project_id INT,
    model_name VARCHAR(32) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT pk_model_id PRIMARY KEY (model_id),
    CONSTRAINT fk_project_id FOREIGN KEY (project_id) REFERENCES project (project_id) ON DELETE SET NULL
);

-- app table creation
CREATE TABLE IF NOT EXISTS app (
    app_id SERIAL,
    project_id INT,
    app_name VARCHAR(32) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT pk_app_id PRIMARY KEY (app_id),
    CONSTRAINT fk_project_id FOREIGN KEY (project_id) REFERENCES project (project_id) ON DELETE SET NULL
);
