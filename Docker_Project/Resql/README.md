# About

Resql, derived from "REST SQL", is one of Bürokratt's generic base components. Such components are called Bükstack components.

Resql is used to create and consume SQL queries as REST calls.

Every query consists of a separate `.sql` file which can be consumed as a REST call. For instance, a valid SQL statement in `/templates/sample-query.sql` is consumed by `https://resql/sample-query`.

# How to use 

## Initial setup
Run the following command in your local computer / virtual server

```mvn spring-boot:run```

## Creating a WAR file
Run the following command in your local computer / virtual server

```mvn clean package```

## Data sources
To manipulate affected databases, edit `sqlms.datasources` parameter values in `application.yml` file and restart the application.

# Documentation

The application creates its own Swagger documentation, which, on your local computer by default, can be found at [http://localhost:8080/swagger-ui/index.html](http://localhost:8080/swagger-ui/index.html).


# Licence

See licence [here](LICENCE.md).
