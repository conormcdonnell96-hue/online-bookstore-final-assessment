import html
from app import BOOKS, cart

def test_checkout_success_happy_path(client):
    cart.clear()
    # Add one item so we can checkout
    client.post("/add-to-cart", data={"title": BOOKS[0].title, "quantity": 1}, follow_redirects=True)

    form = {
        "name": "Test User",
        "email": "test@example.com",
        "address": "123 Test St",
        "city": "Testville",
        "zip_code": "12345",
        "payment_method": "credit_card",
        # Any card NOT ending in 1111 succeeds per mock gateway
        "card_number": "4242 4242 4242 4242",
        "expiry_date": "12/30",
        "cvv": "123",
        "discount_code": "",
    }

    res = client.post("/process-checkout", data=form, follow_redirects=True)
    assert res.status_code == 200

    page = html.unescape(res.data.decode("utf-8"))

    # We landed on the order confirmation page (redirect happens in process_checkout)
    # assert presence of confirmation headings/text instead of the flash string
    assert "Order Confirmed!" in page
    assert "Confirmation Email Sent" in page
    assert "test@example.com" in page

    # after success, cart is cleared (done in process_checkout)
    assert cart.is_empty()
