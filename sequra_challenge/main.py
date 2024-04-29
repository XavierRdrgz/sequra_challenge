import requests
from constants import API_SPACEX_DATA_URL, DB_NAME, SCHEMA
from database import PGDatabase, Table
from model import Launch, LaunchCore, LaunchCrew
import logging


# Returns json data from the spacex launches in a python list of dict
def get_space_x_data():
    with requests.get(API_SPACEX_DATA_URL) as response:
        response.raise_for_status()
        data = response.json()
    logging.info(f"Json data collected from {response.url}")
    return data


def process_json(
    db: PGDatabase, data
) -> tuple[list[Launch], list[LaunchCore], list[LaunchCrew]]:
    launches = []
    launch_cores = []
    launch_crew = []
    for launch in data:
        launch_id = launch["id"]

        cores = launch.pop("cores")
        for core in cores:
            # For some reason there are some core left all null on launch instead of ommited
            if core["core"] is not None:
                core["launch_id"] = launch_id
                launch_cores.append(LaunchCore(**core))

        crew = launch.pop("crew")
        for person in crew:
            person["launch_id"] = launch_id
            launch_crew.append(LaunchCrew(**person))

        launch = Launch(**launch)
        # db.insert_data_test(launch.fairings)
        launches.append(launch)
    logging.info("Records from SpaceX launches processed")

    return (launches, launch_cores, launch_crew)


def create_db_and_tables(db: PGDatabase):
    from os import listdir
    from os.path import isfile, join

    base_path = "./sequra_challenge/sql/tables"
    for f in listdir(base_path):
        f = join(base_path, f)
        if isfile(f):
            with open(f) as table_file:
                create_table = table_file.read()
            db.execute_query(create_table)


def main():
    logging.basicConfig(level=logging.DEBUG)

    # TODO get these from env and secret management
    db_user = "dev"
    db_password = "CHANGE_IN_PROD"
    db_host = "localhost"

    json = get_space_x_data()

    db = PGDatabase().connect(db_user, db_password, db_host, DB_NAME)

    create_db_and_tables(db)

    records = process_json(db, json)

    db.batch_upsert_data(Table(SCHEMA, "launches"), ["id"], records[0])

    db.batch_upsert_data(
        Table(SCHEMA, "launchcores"), ["launch_id", "core"], records[1]
    )

    db.batch_upsert_data(
        Table(SCHEMA, "launchcrews"), ["launch_id", "crew"], records[2]
    )
    logging.info("DONE")
    db.close()


if __name__ == "__main__":
    main()
