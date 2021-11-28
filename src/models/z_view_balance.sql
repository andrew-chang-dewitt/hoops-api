CREATE VIEW balance AS
    SELECT
        SUM(t.amount) AS amount,
        a.name AS collection,
        a.id AS collection_id,
        a.user_id AS user_id
    FROM
        transaction AS t
    INNER JOIN
        account AS a ON a.id = t.account_id
    GROUP BY
        a.name,
        a.id;
