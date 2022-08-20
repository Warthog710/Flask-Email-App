CREATE SCHEMA flask;
SET search_path TO flask, public;

CREATE TABLE "flask".images (
	id BIGSERIAL PRIMARY KEY NOT NULL,
	image_id TEXT NOT NULL,
	image_type TEXT NOT NULL,
	image_data TEXT NOT NULL
);

-- Only for local development databases...
CREATE USER flask_user WITH PASSWORD 'password';
GRANT CONNECT ON DATABASE development TO flask_user;
GRANT USAGE ON SCHEMA flask, public TO flask_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA flask TO flask_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA flask TO flask_user;