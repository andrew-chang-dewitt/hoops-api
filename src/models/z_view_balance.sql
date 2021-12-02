CREATE VIEW account_balance AS
    SELECT
        SUM(t.amount) AS amount,
        a.name AS collection,
        a.id AS collection_id,
        'account' as collection_type,
        a.user_id AS user_id
    FROM
        transaction AS t
    INNER JOIN
        account AS a ON a.id = t.account_id
    GROUP BY
        a.name,
        a.id;

CREATE VIEW envelope_balance AS
    SELECT
        e.total_funds + sum(t.amount) AS amount,
        e.name AS collection,
        e.id AS collection_id,
        'envelope' as collection_type,
        e.user_id AS user_id
    FROM
        envelope as e
    INNER JOIN
        transaction AS t on t.spent_from = e.id
    GROUP BY
        e.total_funds,
        e.name,
        e.id,
        e.user_id;

CREATE VIEW balance AS
    SELECT
        *
    FROM
        account_balance
    UNION
    SELECT
        *
    FROM
        envelope_balance;
