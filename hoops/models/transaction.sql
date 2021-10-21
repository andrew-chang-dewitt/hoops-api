CREATE TABLE IF NOT EXISTS "transaction" (
    "id" uuid PRIMARY KEY,
    "amount" numeric(11, 2) NOT NULL,
    "description" varchar(255) NOT NULL,
    "payee" varchar(255) NOT NULL,
    "date" date NOT NULL
);
