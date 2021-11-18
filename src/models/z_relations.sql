ALTER TABLE "account" 
ADD CONSTRAINT fk_user
    FOREIGN KEY(user_id)
        REFERENCES hoops_user(id)
        ON DELETE CASCADE;
