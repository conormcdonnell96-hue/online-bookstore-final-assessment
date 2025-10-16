from app import BOOKS, cart

def test_checkout_payment_failure_shows_error(client):
    cart.clear()
    # Add one item so checkout is allowed
    client.post("/add-to-cart", data={"title": BOOKS[0].title, "quantity": 1}, follow_redirects=True)

    form = {
        "name": "Test User",
        "email": "test@example.com",
        "address": "123 Test St",
        "city": "Testville",
        "zip_code": "12345",
        "payment_method": "credit_card",
        # Card ending in 1111 triggers failure in the mock gateway
        "card_number": "0000 0000 0000 1111",
        "expiry_date": "12/30",
        "cvv": "123",
        "discount_code": "",
    }

    res = client.post("/process-checkout", data=form, follow_redirects=True)
    assert res.status_code == 200
    assert b"Payment failed" in res.data
