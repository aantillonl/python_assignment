# Take-Home Assignment

**DISCLAIMER**: I only had 1 day to work on this assignment
since I got in touch with the recruiter on Thu, Mar 30, and
could only work on the assignment during one day over the
weekend, thus I didn't get to implement each and all of the
objectives, but I prioritized to implement both tasks in the
more general description of each of them, while overlooking
very speific details

## Design

The project contains a Python module
that does performs a query to the AlphaVantage
API to query stock data for a few companies
and stores this data in a database

The project is structured to be deployed using
Docker and Docker Compose, using the following
containers:

* get_raw_data: Performs a data dump
* db: MySQL Database to store data
* api: API backend to get data and statistics
* adminer: SQL utility to query data directly in SQL

## Run the project
First open `.env` and substitute the APIKEY value for
a real APIKEY.

Then run the project execute the following command:

```bash
docker compose up
```

Docker Compose will build the containers and perform
the data dump. After which the container `get_raw_data`
will perform a data dump

After that data can be inspected directly on adminer
by going to http://localhost:8080, using the user `root`
and the test password `my_password` and db `ctw`.

Also the api is available at:

http://localhost:8081/api/

For some test uris:
* http://localhost:8081/api/financial_data?size=10&symbol=AAPL&start_date=2022-11-11&end_date=2022-11-15
* http://localhost:8081/api/statistics?size=10&symbol=AAPL&start_date=2022-11-11&end_date=2022-11-15

## Considerations

### ORM
This project uses SQL Alchemy to handle the interactions
with the database. ORM provides an easy way to interact
with the DB without having to directly mainulate the db

### FastAPI
This project uses FastAPI to implement the API. FastAPI
provides a quick and simple way to build APIs with a lot
of built-in functionality

## Threading
The data dumper uses threads because it is a suitable
implementation of threads, since it performs multiple
network requests that are I/O bound

## Duplicate Prevention
The DB is desiged to enforce a unique constraint by
symbol name and date, which means that it would not
allow two entries for the same company on the same day

## Exception handling
Exception handling has been implemented in a best effort
way with the allowed time. In the data dumper Exceptions
raised while interacting with the AlphaVantage API are
ignored (they should be at least logged), but it continues
the rest of the requests in case of exceptions.

The API responses are validated against a defined schema,
and then written to the DB. Invalid records are discarded.

DB write exceptions cause the entire transaction to fail.
For example if the data dumer runs again when the data has
already been populated in the DB.

## TODO

* The project structure is not exactly what was stated in the
task
* The API response format has some differences to the one
requested, however al the data can be found, it is just a
matter of data format. I decided to keep it like it this
because it leads to simpler shorter code, and also due to
time constrains, in order to move to the next task.
* Error handling and logging is still premature, could definitely be improved
* Documnetation is vague


## Storage of APIKEY

This repo has a placeholder value for the APIKEY stored
in the .env file. A good solution for this would be to store
it encrypted and have the application decrypt it during
runtime with a key that is protected.

A better solution would be to use a key service like
AWS KMS, which allows application to access keys and
services in AWS. The same could be done for the DB
password with a service like AWS SSM.