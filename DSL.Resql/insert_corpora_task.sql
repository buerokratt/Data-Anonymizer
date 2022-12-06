insert into Corpora_Tasks (raw_text, corpora_id, is_private, created_at) VALUES (:raw_text, :corpora_id, :is_private, :created_at::timestamp) RETURNING id;
