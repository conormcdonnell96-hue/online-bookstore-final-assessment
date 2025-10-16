import html

def test_register_happy_path(client):
    # Create a brand-new user
    form = {
        "name": "Alice Test",
        "email": "alice@example.com",
        "password": "secret123",
        "address": "1 Test Street"
    }
    res = client.post("/register", data=form, follow_redirects=True)
    assert res.status_code == 200

    page = html.unescape(res.data.decode("utf-8"))
    # After successful register, user is logged in and redirected to index
    # Index shows greeting when a user is logged in (Hello, {{ current_user.name }}!)
    assert "Hello, Alice Test!" in page

def test_login_happy_path(client):
    # First register a user
    reg = {
        "name": "Bob Test",
        "email": "bob@example.com",
        "password": "pw123",
        "address": ""
    }
    client.post("/register", data=reg, follow_redirects=True)

    # Log out so we can test login
    client.get("/logout", follow_redirects=True)

    # Login with the same credentials
    res = client.post("/login", data={"email": "bob@example.com", "password": "pw123"}, follow_redirects=True)
    assert res.status_code == 200

    page = html.unescape(res.data.decode("utf-8"))
    assert "Hello, Bob Test!" in page  # confirms session/login worked

def test_account_requires_login_redirects_to_login(client):
    # Not logged in here
    res = client.get("/account", follow_redirects=True)
    assert res.status_code == 200
    page = html.unescape(res.data.decode("utf-8"))
    # We expect to land on the login page and see the friendly flash
    assert "Please log in to access this page." in page
    assert "<title>Login - Online Bookstore</title>" in page
