# Examples

In case of using Resql AS IS without any changes to its default settings and configurations, Resql will initiate its test configurations. As a result, an in-memory database is created with a connection called "test". This allows to test Resql's functionalities out-of-the-box. All of the samples provided below are based on it.

By default, database tables `user` and `user_type` with some entries are created.

>As an initial sample, full curl request is provided. Other samples consist of REST request's JSON body, sample section of response and an equivalent SQL query to get the same result with a pure SQL query.

## Selecting columns (SELECT)

Request : 
```
curl -X POST   http://localhost:8080/test/select   -H 'Content-Type: application/json'   -H 'cache-control: no-cache'   -d '{
	"tableName": "user",
	"columns": ["username", "email"]
}'
```

Equivalent SQL:
```
select username, email
from user
```

Response:
```
[{"username":"user1","email":"user1@example.com"},{"username":"user2","email":"user2@example.com"}]
```

## Limiting response rows (LIMIT)

Request body: 
```
{
	"tableName": "user",
	"columns": ["username", "email"],
	"limit": 1
}
```

Equivalent SQL:
```
select user_name, email
from user 
limit 1
```

Response:
```
[{"username":"user1","email":"user1@example.com"}]
```

## Ordering results (ORDER BY)

Request body: 
```
{
	"tableName": "user",
	"columns": ["username", "email"],
	"orderBy": [{"columnName": "username", "sortOrder": "DESC"}]
}
```
Equivalent SQL:
```
select user_name, first_access_date, document_id 
from document_sharing 
order by first_access_date desc nulls last
```
Response:
```
[{"username":"user2","email":"user2@example.com"},{"username":"user1","email":"user1@example.com"}]
```

## Grouping results (GROUP BY)

Request body: 
```
{
	"tableName": "user",
	"columns": ["user_name", "count(*)"],
	"groups": ["username"]
}
```
Equivalent SQL:
```
select username, count(*) 
from user 
group by username
```
Response:
```
[
[{"username":"user1","count(*)":1},{"username":"user2","count(*)":1}]
```

## Conditional request (WHERE)

Request body: 
```
{
	"tableName": "user",
	"columns": ["username", "email"],
	"condition": "email LIKE 'user2@example.com'"
}
```

>PS! When using curl, JSON content must be escaped
```
"condition": "email LIKE '\''user2@example.com'\''
```

Equivalent SQL:
```
select username, email 
from user 
where (email LIKE 'user2@example.com')
```
Response:
```
[{"username":"user2","email":"user2@example.com"}]
```

## Selecting from multiple tables (JOIN)

Request body: 
```
{
	"tableName": "user",
	"joins": [{"tableName": "user_type", "joinCondition": "user.user_type_id = user_type.id"}],
	"columns": ["username", "user_type", "email"],
}
```
Equivalent SQL:
```
select username, type, email 
from user 
join user_type 
on (user.user_type_id = user_type.id) 
```
Response:
```
[
{"username":"user1","type":"type 1","email":"user1@example.com"},
{"username":"user2","type":"type 2","email":"user2@example.com"}
]
```

## Defining the start of output (OFFSET)

Request body: 
```
{	
	"tableName": "user",
	"columns": ["username", "email"],
	"offset": 1
}
```
Equivalent SQL:
```
select username, email 
from user 
offset 1
```
Response:
```
[{"username":"user2","email":"user2@example.com"}]
```

## Adding new rows (INSERT)

>The following sample query is made towards `POST /test/insert` REST API endpoint

request body:
```
{
	"tableName": "user",
	"columnValueMaps": [
		{
            "id" : 3,
		    "username": "user3", 
		    "email": "user3@example.com",
            "name": "User Number 3",
            "user_type_id" : 1
            
	    }, 
		{
            "id" : 4,
		    "username": "user4", 
		    "email": "user4@example.com",
            "name": "User Number 4",
            "user_type_id" : 2           
	    }
	]
}

```

Equivalent SQL:
```
INSERT INTO user (id, username, email, name, user_type_id)
VALUES (3, 'user3', 'user3@example.com', 'User Number 3', 1), (4, 'user4', 'user4@example.com', 'User Number 4', 2);
```
Response:
```
2
```

## Additional functionality to add specifically just 1 row (INSERT)

>The following sample query is made towards `POST /portaal/singleInsert` REST API endpoint

A special functionality to allow inserting just 1 row without using arrays.

request body:
```
{
	"tableName": "epost.eaadressid",
	"columnValueMap": {
		"aadress": "leet_haxxor@aol.com",
		"aktiveeritud": true
	}
}
```

Equivalent SQL:
```
insert into "epost.eaadressid" (aadress, aktiveeritud) 
values ('leet_haxxor@aol.com', true)
```
Response:
```
1
```

## Updating existing values (UPDATE)

>The following sample query is made towards `PATCH /adit/update` REST API endpoint


Request body:
```
{
	"tableName": "document_type",
	"columnValueMap": {
		"short_name": "Word", 
		"description": "Wordi dokument"
	},
	"condition": "short_name = 'text'"
}
```
Equivalent SQL:
```
update "document_type" 
set short_name = 'Word', description = 'Wordi dokument' 
where (short_name = 'text')
```
Response:
```
2
```
