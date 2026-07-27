import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the /health endpoint returns 200 and correct payload."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'user-management-api'

def test_get_users(client):
    """Test the /api/v1/users endpoint returns user list."""
    response = client.get('/api/v1/users')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) > 0