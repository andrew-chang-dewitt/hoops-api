ALTER TABLE "envelope" 
ADD CONSTRAINT fk_user
    FOREIGN KEY(user_id)
        REFERENCES hoops_user(id)
        ON DELETE CASCADE;

ALTER TABLE "account" 
ADD CONSTRAINT fk_user
    FOREIGN KEY(user_id)
        REFERENCES hoops_user(id)
        ON DELETE CASCADE;

ALTER TABLE "transaction" 
ADD CONSTRAINT fk_user
    FOREIGN KEY(account_id)
        REFERENCES account(id)
        ON DELETE CASCADE;
