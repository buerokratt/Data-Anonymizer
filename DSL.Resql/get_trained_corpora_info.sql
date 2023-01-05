select corpora_id, source_file_name, source_file_size, created_at, trained_at from Corpora_Info where trained_at is not null order by trained_at desc limit 1;
