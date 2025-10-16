import pytest
from app import BOOKS, cart

@pytest.mark.xfail(reason="Setting quantity to 0 does not remove the item from the cart (current behavior)")
def test_update_cart_zero_should_remove_item(client):
    cart.clear()
    book = BOOKS[0]

    # Add one item first
    client.post("/add-to-cart", data={"title": book.title, "quantity": 1}, follow_redirects=True)

    # Now set quantity to 0 (expected: item removed, cart empty)
    res = client.post(
        "/update-cart",
        data={"title": book.title, "quantity": 0},
        follow_redirects=True,
    )
    assert res.status_code == 200

    # Expected once fixed: cart is empty
    assert cart.is_empty()
