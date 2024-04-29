

### Installation

I use [`poetry`](https://python-poetry.org/docs/#installation) to handle everything in python and dbt.

On mac I needed to install `postgresql` to use `psycopg2`

```bash
> brew install postgresql
```

It might be necessary to install `libpq-dev` or `postgresql-devel` on linux depending on the distro.

### Usage

First run docker compose to get postgres up and running

```bash
> docker compose up
```

To run the python code

```bash
poetry run python ./sequra_challenge/main.py
```

Run [`dbt`](https://docs.getdbt.com/docs/get-started-dbt) to build layers on top of the raw data

```bash
> poetry run dbt
```

And use dbt compile to generate the sql files that answer the 3 analytics questions.
The compiled files can be found in `./target/compiled/analysis`

```bash
> poetry run compile
```

To test the code

```bash
> poetry run pytest
```

To test the dbt models

```bash
> poetry run dbt test
```

### Project walkthrough

The solution proposed has a raw data collection step with the Python code and `dbt` to model the data with layers on top.

The python code calls the Spacexdata API to gather the launch data parses the json and does some minor processing to ensure that we can insert it in some reasonable tables in postgres. Data validation at these steps consists of:
    - Parsing the json to ensure it's valid
    - Using Pydantic models to ensure the fields have the consistent types (if a field is a boolean it's always a boolean).
    
Any data failure at this step should be because the API has broken it's contract with the data format (json) or the schema they are providing.

With dbt we then model the data once it's in the database. In this project, not much needs to be done because the source data itself is pretty good and there isn't extra sources to aggregate. The first layer, called staging (stg), is used for
data standardization by changing names and enforcing types (like dates and timestamp parsing from strings). We could have an intermediate layer to aggregate with other sources or do extra transformations but it's not needed in this case.
Finally the mart layer provides materialized tables of the data for analytics consumption.

### Data quality

To ensure data quality the raw ingestion layer in python should do minimal processing to insert into the database. At this
stage we can check for validation of the data format that comes from the source (in case of json there's not many guarantees provided). Logging is added in the code that should be expanded and properly configured to use as alerts when something goes wrong.

In the case of the Spacex launches source there seems to be all the data always available. In another case, when dealing with more volatile APIs when calling them gives the data for this particular moment in time, we might want to store the json files in some cloud storage like S3, HDFS or equivalent in other cloud providers.

Dbt provides facilities for testing for data staleness that should add another alert in case the data acquisition is not running at all. One option is to add a `last_updated` field to every raw table and make dbt test that.

With this if any alert happens it should be pretty clear where the error ocurred and how to start debugging and fixing it.

### Cloud deployment

This solution is pretty agnostic in what cloud or architecture you can use with it. To deploy this in a production environment it would need:
    - A way to handle env variables and config like (services urls, database names, etc)
    - A secret manager to store and access database credentials
    - Some kind of cron scheduler to run the python code like (kubernetes cron, crontab in a cloud vm, airflow, etc)
    - Dbt cloud or some adhoc setup equivalent to run `dbt`, `dbt test`, `dbt source freshness` and store the dbt website with the docs.

### Data Model

Some considerations about the data model:
    - The names from the entities LaunchCores and LaunchCrew are not accidental. This represent data associated to the relationship between Launch and Cores and Launch and Crew. There are other endpoints that better represent the Cores and Crew entities and we might want to gather in the future.
    - Very few data is actually needed to solve the questions proposed. But since the data source is so small there's very little overhead to store everything from Spacex launches. In the case of some more involved fields I made the decision to store them as a json fields to skip the modeling part while ensuring we can use the data later if we want. Although, I haven't been able to store json fields with psycopg2 when they are accompanied of other fields.
