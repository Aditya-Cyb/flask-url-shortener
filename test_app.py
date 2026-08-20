import pytest
from app import app, url_map

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        url_map.clear()  # Har test se pehle clean state
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_shorten_url(client):
    response = client.post('/shorten', json={"url": "https://www.example.com"})
    assert response.status_code == 201
    data = response.get_json()
    assert "short_code" in data
    assert data["original_url"] == "https://www.example.com"

def test_shorten_url_missing_field(client):
    response = client.post('/shorten', json={})
    assert response.status_code == 400

def test_redirect(client):
    # Pehle ek short URL banao
    post_response = client.post('/shorten', json={"url": "https://www.example.com"})
    short_code = post_response.get_json()["short_code"]
    
    # Ab redirect test karo
    get_response = client.get(f'/{short_code}')
    assert get_response.status_code == 302  # redirect status code
    assert get_response.location == "https://www.example.com"

def test_redirect_not_found(client):
    response = client.get('/nonexistent123')
    assert response.status_code == 404

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"