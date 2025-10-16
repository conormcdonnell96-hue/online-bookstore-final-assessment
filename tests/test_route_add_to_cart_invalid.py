import pytest
from app import BOOKS

@pytest.mark.xfail(reason="Non-numeric quantity raises ValueError in add_to_cart (current behavior)")
def test_add_to_cart_non_numeric_quantity_is_handled(client):
    # Send 'abc' for quantity; current code: quantity = int(request.form.get('quantity', 1))
    res = client.post(
        "/add-to-cart",
        data={"title": BOOKS[0].title, "quantity": "abc"},
        follow_redirects=True,
    )
    # Expected (once fixed): 200 and a friendly flash.
    # For now this test is xfail to document the bug without breaking CI.
    assert res.status_code == 200
