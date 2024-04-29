from typing import Self, TypeVar
import psycopg2
import psycopg2.extras
import psycopg2.sql as sql
from psycopg2 import OperationalError
import logging
from dataclasses import dataclass

from pydantic import BaseModel

T = TypeVar("T")

psycopg2.extensions.register_adapter(dict, psycopg2.extras.Json)


@dataclass
class Table:
    schema: str
    table: str

    def sql_identifier(self):
        return sql.SQL(".").join(
            (sql.Identifier(self.schema), sql.Identifier(self.table))
        )


class PGDatabase:
    connection = None

    def close(self):
        if self.connection is not None:
            self.connection.close()

    def connect(
        self,
        db_user: str,
        db_password: str,
        db_host: str,
        db_name: str = "postgres",
        db_port: int = 5432,
    ) -> Self:
        try:
            self.connection = psycopg2.connect(
                database=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
            )
            logging.info("Connection to PostgreSQL DB successful")
        except OperationalError as e:
            logging.error(f"The error '{e}' occurred")
        return self

    def execute_query(self, query, autocommit=True):
        self.connection.autocommit = autocommit
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query)
                logging.debug(f"Query:\n{query}")
                logging.info("Query executed successfully")
            except OperationalError as e:
                logging.error(f"The error '{e}' occurred")

    def fetchone(self, query):
        self.connection.autocommit = True
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query)
                data = cursor.fetchone()
                logging.info("Query executed successfully")
            except OperationalError as e:
                logging.error(f"The error '{e}' occurred")

        return data

    def insert_data(self, table: Table, data: list[BaseModel]):
        if len(data) > 0:
            fields = data[0].model_fields.keys()

            insert_query = sql.SQL(
                "INSERT INTO {table} ({fields}) VALUES ({placeholders})"
            ).format(
                table=table.sql_identifier(),
                fields=sql.SQL(", ").join(map(sql.Identifier, fields)),
                placeholders=sql.SQL(", ").join(map(sql.Placeholder, fields)),
            )

            self.connection.autocommit = False
            with self.connection.cursor() as cursor:
                count = 0
                try:
                    for elem in data:
                        data_values = elem.model_dump()
                        logging.debug(
                            f"Executing query: {cursor.mogrify(insert_query, data_values)}"
                        )
                        cursor.execute(insert_query, data_values)
                        count += cursor.rowcount
                    self.connection.commit()

                    logging.info(
                        f"{count} records inserted successfully in table '{table}'"
                    )
                except OperationalError as e:
                    self.connection.rollback()
                    logging.error(f"The error '{e}' occurred")

    def batch_upsert_data(
        self, table: Table, primary_key: list[str], data: list[BaseModel]
    ):
        if len(data) > 0:
            fields = data[0].model_fields.keys()

            upsert_query = sql.SQL(
                """
INSERT INTO {table} ({fields})
VALUES ({placeholders})
ON CONFLICT({primary_key})
DO UPDATE SET
  {fields_update}
    """
            ).format(
                table=table.sql_identifier(),
                fields=sql.SQL(", ").join(map(sql.Identifier, fields)),
                placeholders=sql.SQL(", ").join(map(sql.Placeholder, fields)),
                primary_key=sql.SQL(", ").join(map(sql.Identifier, primary_key)),
                fields_update=sql.SQL(",\n  ").join(
                    [
                        sql.SQL(" = EXCLUDED.").join([sql.Identifier(field)] * 2)
                        for field in fields
                        if field not in primary_key
                    ]
                ),
            )

            self.connection.autocommit = False
            with self.connection.cursor() as cursor:
                count = 0
                try:
                    for elem in data:
                        data_values = elem.model_dump()
                        logging.debug(
                            f"Executing query: {cursor.mogrify(upsert_query, data_values)}"
                        )
                        cursor.execute(upsert_query, data_values)
                        count += cursor.rowcount
                    self.connection.commit()
                    logging.info(
                        f"{count} records affected in table {table.sql_identifier().as_string(self.connection)}"
                    )
                except OperationalError as e:
                    self.connection.rollback()
                    logging.error(f"The error '{e}' occurred")
