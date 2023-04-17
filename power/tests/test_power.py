import pytest
from server import api
import json


def test_power():
    response = api.test_client().post('/power', json={"base" : 2, 'exponent':3})
    data = json.loads(response.data)
    status_code = response.status_code

    assert status_code == 200
    assert data['power'] == 8

def test_power_base0():
    response = api.test_client().post('/power', json={"base" : 0, 'exponent':3})
    status_code = response.status_code

    assert status_code == 400

def test_power_wrong_value():
    response = api.test_client().post('/power', json={"base" : 'test', 'exponent':'test2'})
    status_code = response.status_code

    assert status_code == 400
