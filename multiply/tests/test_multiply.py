import pytest
from server import api
import json


def test_multiply():
    response = api.test_client().post('/multiply', json={"numbers" : [4, 3, 2, 1]})
    data = json.loads(response.data)
    status_code = response.status_code

    assert status_code == 200
    assert data['multiply'] == 24

def test_multiply_wrong_value():
    response = api.test_client().post('/multiply', json={"numbers" : 'test_value'})
    status_code = response.status_code

    assert status_code == 400
