SELECT user_id, array_agg(due_by) due_dates
FROM debt
WHERE user_id = :userId
GROUP BY user_id;
