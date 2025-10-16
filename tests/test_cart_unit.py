from models import Book, Cart

def test_cart_add_and_totals():
    cart = Cart()
    b1 = Book("Gatsby", "Fiction", 10.99, "images/books/the_great_gatsby.jpg")
    b2 = Book("1984", "Dystopia", 8.99, "images/books/1984.jpg")

    cart.add_book(b1, 2)   # 2 * 10.99 = 21.98
    cart.add_book(b2, 3)   # 3 * 8.99  = 26.97

    assert cart.get_total_items() == 5
    # float-safe comparison
    assert abs(cart.get_total_price() - (21.98 + 26.97)) < 1e-9
