SET timezone = 'UTC';

CREATE TABLE IF NOT EXISTS "transaction" (
    "id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "amount" NUMERIC(11, 2) NOT NULL,
    "description" TEXT,
    "payee" TEXT NOT NULL,
    "timestamp" TIMESTAMPTZ NOT NULL,
    "account_id" UUID NOT NULL
);
