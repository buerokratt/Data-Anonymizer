CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TABLE IF NOT EXISTS Corpora_Info (corpora_id VARCHAR PRIMARY KEY, source_file_name varchar, source_file_size varchar, created_at timestamp NOT NULL DEFAULT NOW(), trained_at timestamp, active BOOLEAN DEFAULT TRUE);
CREATE TABLE IF NOT EXISTS Entity (name varchar NOT NULL UNIQUE, description varchar NULL);
CREATE TABLE IF NOT EXISTS Regex_Entity (id SERIAL, regex varchar NOT NULL, entity varchar NOT NULL, active BOOLEAN DEFAULT TRUE, created_at timestamp NOT NULL DEFAULT NOW());
CREATE TABLE IF NOT EXISTS Corpora_Tasks (id SERIAL, corpora_id VARCHAR, is_private BOOLEAN, raw_text VARCHAR, sentences_annotations JSON, created_at timestamp NOT NULL DEFAULT NOW());
CREATE OR REPLACE FUNCTION list_corpora_tasks_paginated(where_condition varchar, sort_condition varchar, page varchar, page_size varchar )
RETURNS TABLE(id int, corpora_id varchar, is_private boolean, raw_text varchar, created_at timestamp, full_count bigint, predictions text) AS $$
BEGIN
  RETURN QUERY EXECUTE FORMAT('select Corpora_Tasks."id", Corpora_Tasks."corpora_id", Corpora_Tasks."is_private", Corpora_Tasks."raw_text", Corpora_Tasks."created_at", count(*) OVER() AS full_count, Corpora_Tasks."sentences_annotations"::text AS predictions from Corpora_Tasks join (select Corpora_Tasks."id", max(Corpora_Tasks."created_at") as most_recent_task from Corpora_Tasks group by id) p ON (Corpora_Tasks.id = p.id and Corpora_Tasks.created_at = p.most_recent_task) where %s order by %s LIMIT %s OFFSET ((%s - 1) * %s)', where_condition, sort_condition, page_size, page, page_size);
END;
$$ LANGUAGE plpgsql;