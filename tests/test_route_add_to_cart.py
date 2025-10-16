import html
from app import BOOKS, cart

def test_add_to_cart_happy_path(client):
    cart.clear()
    book = BOOKS[0]

    res = client.post(
        "/add-to-cart",
        data={"title": book.title, "quantity": 2},
        follow_redirects=True,
    )

    assert res.status_code == 200

    # Jinja will HTML-escape quotes, so decode + unescape first
    text = html.unescape(res.data.decode("utf-8"))

    # Now this matches the flashed string emitted by app.py
    expected = f'Added 2 "{book.title}" to cart!'
    assert expected in text

    # And the cart count should reflect it
    assert cart.get_total_items() == 2
