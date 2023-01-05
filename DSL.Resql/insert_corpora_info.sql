insert into Corpora_Info (corpora_id, source_file_name, source_file_size) VALUES (uuid_generate_v4(), :source_file_name, :source_file_size) RETURNING corpora_id, created_at;
