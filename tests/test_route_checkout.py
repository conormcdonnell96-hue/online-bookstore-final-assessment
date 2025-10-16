from app import cart

def test_checkout_empty_cart_redirects(client):
    # Ensure cart is empty
    cart.clear()

    # Hit /checkout and follow redirects so we land back on index
    res = client.get("/checkout", follow_redirects=True)

    assert res.status_code == 200
    # Flash message content from app.py when cart is empty
    assert b"Your cart is empty!" in res.data
