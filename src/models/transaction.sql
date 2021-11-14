SET timezone = 'UTC';

CREATE TABLE IF NOT EXISTS "transaction" (
    "id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "amount" NUMERIC(11, 2) NOT NULL,
    "description" VARCHAR(255) NOT NULL,
    "payee" VARCHAR(255) NOT NULL,
    "timestamp" TIMESTAMPTZ NOT NULL
);
