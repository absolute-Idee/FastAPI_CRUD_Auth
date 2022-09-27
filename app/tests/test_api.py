from fastapi.testclient import TestClient

from app.backend.api import app

from app.backend.auth.utils import verify_password



client = TestClient(app)

def test_get_posts(client: TestClient):
    response = client.get("/posts")

    assert response.status_code == 200
    assert response.json()[0]['text'] == 'qwerty'
    
def test_sign_up(client: TestClient): 
    request_data = {
        'username': 'admin26',
        'password': 'admin26',
    }

    response = client.post('/signup', json=request_data)
    assert response.status_code == 200
    assert verify_password('admin26',response.json()['password'])
    assert response.json()['username'] == 'admin26'
    

def test_user_detail_forbidden_without_token(client: TestClient):
    response = client.get('/me')
    assert response.status_code == 401
