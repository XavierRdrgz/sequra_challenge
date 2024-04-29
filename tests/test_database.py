import logging

from pydantic import BaseModel
from sequra_challenge.database import PGDatabase, Table
from sequra_challenge.constants import DB_NAME

db_user = "dev"
db_password = "CHANGE_IN_PROD"
db_host = "localhost"

db = PGDatabase().connect(db_user, db_password, db_host, DB_NAME)
db.execute_query("""CREATE SCHEMA IF NOT EXISTS "test" """)


class TestModel(BaseModel):
    __test__ = False
    a: int
    b: str


table = Table("test", "test")


def test_insert_data():
    logging.basicConfig(level=logging.DEBUG)

    db.execute_query(
        """DROP TABLE IF EXISTS "test"."test"; CREATE TABLE "test"."test" ( "a" integer, "b" character varying)"""
    )

    data = [TestModel(a=3, b="three"), TestModel(a=42, b="fortytwo")]
    db.insert_data(table, data)
    result = db.fetchone("""SELECT b FROM "test"."test" WHERE "a" = 3""")

    assert result[0] == "three"


def test_upsert_data():
    logging.basicConfig(level=logging.DEBUG)

    db.execute_query(
        """DROP TABLE IF EXISTS "test"."test"; CREATE TABLE "test"."test" ( "a" integer, "b" character varying, CONSTRAINT "test_pkey" PRIMARY KEY ("a"))"""
    )

    data = [TestModel(a=3, b="three"), TestModel(a=42, b="fortytwo")]
    db.batch_upsert_data(table, ["a"], data)
    data = [TestModel(a=42, b="Fortytwo")]
    db.batch_upsert_data(table, ["a"], data)
    result = db.fetchone("""SELECT b FROM "test"."test" WHERE "a" = 42""")

    assert result[0] == "Fortytwo"
