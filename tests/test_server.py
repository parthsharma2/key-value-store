import unittest
import pytest

from kvs import server


@pytest.fixture
def client():
    server.app.config['TESTING'] = True

    with server.app.test_client() as client:
        yield client

def test_server_ping(client):
    res = client.get('/api/ping')
    assert res.status_code == 200
    assert res.json['status'] == 'ok'

def test_server_set(client):
    res = client.post('/api/hello', json={'value': 'world'})
    assert res.status_code == 200
    assert res.json['result'] == 'hello:world stored successfully'

def test_server_get_existant_key(client):
    client.post('/api/hello', json={'value': 'world'})

    res = client.get('/api/hello')
    assert res.status_code == 200
    assert res.json['result'] == 'world'

def test_server_get_non_existant_key(client):
    res = client.get('/api/jello')
    assert res.status_code == 200
    assert res.json['result'] == 'null'

def test_server_delete_existant_key(client):
    client.post('/api/hello', json={'value': 'world'})

    res = client.delete('/api/hello')
    assert res.status_code == 200
    assert res.json['result'] == 'hello deleted'

def test_server_delete_non_existant_key(client):
    res = client.delete('/api/hello')
    assert res.status_code == 200
    assert res.json['result'] == 'hello does not exist'

def test_server_responds_with_400_with_incorrect_set_request(client):
    res = client.post('/api/test')
    assert res.status_code == 400

    res = client.post('/api/test', data='non json data')
    assert res.status_code == 400

    res = client.post('/api/test', json={'val': 'abc'})
    assert res.status_code == 400

def test_server_handles_404(client):
    res = client.get('/something')
    assert res.status_code == 404