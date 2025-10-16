def test_homepage_loads(client):
    """Simple smoke test for the index route"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"<html" in response.data.lower()
