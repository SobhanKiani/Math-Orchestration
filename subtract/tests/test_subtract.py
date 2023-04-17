import pytest
from server import api
import json


def test_subtract():
    response = api.test_client().post('/subtract', json={"numbers" : [3,2,1]})
    data = json.loads(response.data)
    status_code = response.status_code

    assert status_code == 200
    assert data['subtract'] == 0

def test_subtract_wrong_value():
    response = api.test_client().post('/subtract', json={"numbers" : 'test'})
    status_code = response.status_code

    assert status_code == 400
    
