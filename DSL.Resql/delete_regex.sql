insert into Regex_Entity (id, regex, entity, active) select id, regex, entity, False from Regex_Entity where id = :id ORDER BY created_at DESC limit 1;
