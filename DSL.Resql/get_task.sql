select id, corpora_id, created_at, is_private, raw_text, sentences_annotations::text AS predictions from Corpora_Tasks where corpora_id = :corpora_id and id = :id ORDER BY created_at DESC limit 1;
