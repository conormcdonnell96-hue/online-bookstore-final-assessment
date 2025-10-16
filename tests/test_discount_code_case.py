import html
import pytest
from app import BOOKS, cart

@pytest.mark.xfail(reason="Discount codes are case-sensitive; 'save10' should work but doesn't yet")
def test_discount_code_lowercase_expected_discount(client, capsys):
    cart.clear()
    # Add a single item (The Great Gatsby is 10.99)
    client.post("/add-to-cart", data={"title": BOOKS[0].title, "quantity": 1}, follow_redirects=True)

    form = {
        "name": "Case Test",
        "email": "case@example.com",
        "address": "123 Test St",
        "city": "Testville",
        "zip_code": "12345",
        "payment_method": "credit_card",
        "card_number": "4242 4242 4242 4242",  # succeeds
        "expiry_date": "12/30",
        "cvv": "123",
        "discount_code": "save10",              # lowercase on purpose
    }

    # Perform checkout (follow redirects to confirmation page)
    res = client.post("/process-checkout", data=form, follow_redirects=True)
    assert res.status_code == 200

    # EmailService prints total amount; capture stdout and assert 10% off applied
    # 10.99 * 0.90 = 9.891 -> shown as $9.89
    captured = capsys.readouterr().out
    assert "Total Amount: $9.89" in captured
