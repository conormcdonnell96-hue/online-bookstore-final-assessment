import os
import timeit
import cProfile, pstats, io

import pytest
from models import Book, Cart

# Only runs when PERF=1 is set so CI stays fast/green
pytestmark = pytest.mark.skipif(os.getenv("PERF") != "1", reason="Set PERF=1 to run perf baseline locally")

def _build_sample_cart():
    cart = Cart()
    # Build a moderately sized cart: 4 titles with varying quantities
    titles = [
        ("The Great Gatsby", "Fiction", 10.99, "images/books/the_great_gatsby.jpg", 5),
        ("1984", "Dystopia", 8.99, "images/books/1984.jpg", 7),
        ("I Ching", "Traditional", 18.99, "images/books/I-Ching.jpg", 2),
        ("Moby Dick", "Adventure", 12.49, "images/books/moby_dick.jpg", 4),
    ]
    for title, cat, price, img, qty in titles:
        cart.add_book(Book(title, cat, price, img), qty)
    return cart

def test_perf_baseline_timeit_and_cprofile():
    cart = _build_sample_cart()

    # --- timeit baseline ---
    stmt = "cart.get_total_price()"
    setup = "from __main__ import cart"
    # Use timeit's callable form to avoid globals hassle
    times = timeit.repeat(lambda: cart.get_total_price(), repeat=5, number=500)
    best = min(times)
    per_call_ms = (best / 500) * 1000.0
    print(f"[timeit] best={best:.6f}s over 500 runs → {per_call_ms:.4f} ms/call")

    # --- cProfile hotspot snapshot ---
    pr = cProfile.Profile()
    pr.enable()
    for _ in range(500):
        cart.get_total_price()
    pr.disable()

    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats(pstats.SortKey.TIME)
    ps.print_stats(10)  # top 10 entries
    print("[cProfile]\n" + s.getvalue())

