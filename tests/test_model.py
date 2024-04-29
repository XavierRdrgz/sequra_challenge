from typing import List
import pydantic

from sequra_challenge import model


def test_json_parsing():
    ta = pydantic.TypeAdapter(List[model.Launch])
    ta.validate_json
    with open("./tests/data/spacexdata_launches.json") as f:
        data = f.read()

        launches = ta.validate_json(data)

    launches_json_str = ta.dump_json(launches)
    launches_2 = ta.validate_json(launches_json_str)
    assert launches == launches_2
