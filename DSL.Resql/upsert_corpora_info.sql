insert into Corpora_Info (corpora_id, source_file_name, source_file_size, trained_at) select corpora_id, source_file_name, source_file_size, current_timestamp from Corpora_Info where corpora_id=:corpora_id ORDER BY created_at DESC limit 1;
