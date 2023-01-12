INSERT INTO debt (user_id, amount, due_by)
VALUES (:userId, :amount, cast(:dueBy AS TIMESTAMP WITH TIME ZONE));
