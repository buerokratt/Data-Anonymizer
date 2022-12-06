insert into Corpora_Tasks (id, raw_text, corpora_id, is_private, sentences_annotations) select :id, raw_text, corpora_id, is_private, :sentences_annotations::json from Corpora_Tasks where corpora_id=:corpora_id and id=:id ORDER BY created_at DESC limit 1 RETURNING id;