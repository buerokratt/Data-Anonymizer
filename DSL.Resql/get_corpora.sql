SELECT id, corpora_id, created_at, full_count, is_private, predictions, raw_text FROM list_corpora_tasks_paginated(:where_condition, :sort_condition, :page, :page_size);
