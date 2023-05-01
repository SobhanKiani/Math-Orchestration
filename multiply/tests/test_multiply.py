import pytest
from server import api
import json


def test_multiply():
    response = api.test_client().post('/multiply', json={"a": 2, "c": 6})
    data = json.loads(response.data)
    status_code = response.status_code

    assert status_code == 200
    assert data['2a'] == 4
    assert data['4ac'] == 48


def test_multiply_wrong_value():
    response = api.test_client().post('/multiply', json={"a" : 'test_value', 'c': "test_value2"})
    status_code = response.status_code

    assert status_code == 400
