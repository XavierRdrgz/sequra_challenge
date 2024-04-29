from unittest.mock import Mock
from sequra_challenge.main import main


def test_main_runs():
    requests = Mock()
    json = open("./tests/data/spacexdata_launches.json").read()
    requests.get.return_value = json
    main()
    # Test main runs without exceptions with mock data
    assert True
