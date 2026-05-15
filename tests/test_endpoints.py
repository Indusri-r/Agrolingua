import pytest
from app import app

@pytest.fixture

def client():
    with app.test_client() as c:
        yield c


def test_predict_plant_requires_input(client):
    resp = client.get('/predict-plant')
    assert resp.status_code == 200
    assert 'error' in resp.json
    assert 'soil' in resp.json['error'].lower()


def test_predict_plant_with_data(client):
    params = {
        'soil_moisture': '50',
        'temperature': '25',
        'ph_level': '7',
        'npk_n': '40',
        'npk_p': '20',
        'npk_k': '30',
        'ec': '1',
        'co2': '400'
    }
    resp = client.get('/predict-plant', query_string=params)
    assert resp.status_code == 200
    assert 'prediction' in resp.json
    assert 'audio_url' in resp.json


def test_biofertilizer_endpoint(client):
    resp = client.get('/biofertilizer')
    assert resp.status_code == 200
    assert 'error' in resp.json

    resp2 = client.get('/biofertilizer', query_string={'crop': 'rice'})
    assert resp2.status_code == 200
    assert 'suggestions' in resp2.json
    assert isinstance(resp2.json['suggestions'], list)
    assert 'audio_url' in resp2.json
