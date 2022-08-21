from .config import *

def test_status():
    response = client.get("/status")

    data = response.json()

    assert response.status_code == 200
    assert data["message"] == 'ok'

def test_get_item():
    response = client.get("/items/1")
    
    data = response.json()

    assert response.status_code == 200, response.text
    assert data.get("id") == 1
    assert data.get("title") == 'Test'
