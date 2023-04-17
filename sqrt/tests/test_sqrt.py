import pytest
from server import api
import json


def test_sqrt():
    response = api.test_client().post('/sqrt', json={"number" : 49})
    data = json.loads(response.data)
    status_code = response.status_code

    assert status_code == 200
    assert data['sqrt'] == 7

def test_sqrt_negative_number():
    response = api.test_client().post('/sqrt', json={"number" : -1})
    status_code = response.status_code

    assert status_code == 400


def test_sqrt_string_value():
    response = api.test_client().post('/sqrt', json={"number" : 'test'})
    status_code = response.status_code

    assert status_code == 400
