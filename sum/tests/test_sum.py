import pytest
from server import api
import json


def test_sum():
    response = api.test_client().post('/sum', json={"numbers" : [1, 2, 3]})
    data = json.loads(response.data)
    status_code = response.status_code

    assert status_code == 200
    assert data['sum'] == 6

def test_sum_wrong_value():
    response = api.test_client().post('/sum', json={"numbers" : 'test'})
    status_code = response.status_code

    assert status_code == 400
    
