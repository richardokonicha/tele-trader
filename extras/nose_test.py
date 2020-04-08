
#%%
import requests
from nose.tools import assert_true
#%%

# def test_request_response():
#     response = requests.get('http://jsonplaceholder.typicode.com/todos')
#     assert_true(response.ok)

# test_request_response()
# nosetests --verbosity=2 nose_test.py


#%%
BASE_URL = 'http://jsonplaceholder.typicode.com/todos'

def parser():
    response = requests.get(BASE_URL)
    resp = response.json
    return resp

from nose.tools import assert_is_not_none

def test_request_response():
    response = parser()
    
    assert_is_not_none(type(response) == dict())

