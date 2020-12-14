# Housing API

A simple housing API built with Flask and MongoDB

## Run the project

The easiest way to run the project is with `docker-compose`.
To be able to run the app, you need to create .env files for the environment variables.
Here is an example:

`.env.development`

```
SECRET_KEY=test-secret-key
DB_USER=testuser
DB_PWD=testpassword
DB_HOST=database
DB_NAME=housing
```

`database/.env.development`

```
MONGO_INITDB_ROOT_USERNAME=testuser
MONGO_INITDB_ROOT_PASSWORD=testpassword
MONGO_INITDB_DATABASE=housing
```

After creating these files, run

```
docker-compose -f docker-compose.dev.yml up
```
