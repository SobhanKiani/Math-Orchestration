import pytest
from server import api
import json


def test_division():
    response = api.test_client().post('/division', json={"numbers" : [12, 2, 3]})
    data = json.loads(response.data)
    status_code = response.status_code

    assert status_code == 200
    assert data['division'] == 2


def test_division_0():
    response = api.test_client().post('/division', json={"numbers" : [12, 0, 2, 3]})
    status_code = response.status_code
    assert status_code == 400

def test_division_wrong_value():
    response = api.test_client().post('/division', json={"numbers" : "string"})
    status_code = response.status_code    

    assert status_code == 400

