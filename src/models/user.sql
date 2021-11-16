SET timezone = 'UTC';

CREATE EXTENSION pgcrypto;

CREATE TABLE IF NOT EXISTS "hoops_user" (
    "id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "handle" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "full_name" TEXT NOT NULL,
    "preferred_name" TEXT
);
