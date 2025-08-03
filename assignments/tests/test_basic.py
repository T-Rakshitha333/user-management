import os
import sys
from urllib.parse import urlparse
import pytest
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
sys.path.insert(0, APP_DIR)
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_shorten_valid_url(client):
    response = client.post('/api/shorten', json={"url": "https://example.com"})
    assert response.status_code == 201
    data = response.get_json()
    assert "short_code" in data
    assert "short_url" in data
    assert urlparse(data["short_url"]).scheme in ("http", "https")

def test_shorten_invalid_url(client):
    response = client.post('/api/shorten', json={"url": "invalid_url"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_redirect_and_click_count(client):
    # Step 1: Create short URL
    shorten_resp = client.post('/api/shorten', json={"url": "https://example.org"})
    data = shorten_resp.get_json()
    short_code = data["short_code"]
    short_url = data["short_url"]

    # Step 2: Access short URL
    redirect_resp = client.get(f'/{short_code}', follow_redirects=False)
    assert redirect_resp.status_code == 302
    assert redirect_resp.headers['Location'] == "https://example.org"

    # Step 3: Check analytics
    stats_resp = client.get(f'/api/stats/{short_code}')
    stats = stats_resp.get_json()
    assert stats_resp.status_code == 200
    assert stats["url"] == "https://example.org"
    assert stats["clicks"] == 1
    assert "created_at" in stats

def test_redirect_not_found(client):
    response = client.get('/invalid123')
    assert response.status_code == 404
    assert "error" in response.get_json()

def test_stats_not_found(client):
    response = client.get('/api/stats/invalid123')
    assert response.status_code == 404
    assert "error" in response.get_json()
