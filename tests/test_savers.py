import json
import os

from src.savers import SaverJson

test_data_json = [{"query": "value", "count": 7}]
test_file = "./data/test_json.json"
if os.getcwd().split("/")[-1] == "tests":
    test_file = "../data/test_json.json"


def test_write_json():
    testwrite = SaverJson(test_file, test_data_json)
    testwrite.save_to_file()
    with open(test_file, "r") as jsonfile:
        result_data_json = json.load(jsonfile)
    assert test_data_json == result_data_json
