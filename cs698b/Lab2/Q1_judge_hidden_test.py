import pytest
from Q1 import ganitagya

def assert_exact_match( submitted, gold ):
    assert set( submitted.keys() ) == set( gold.keys() )
    assert submitted == gold

def test_1():
    n = 10
    gold = {
        "even_digits": [ 0 ],
        "is_parity_ordered": True,
        "subset_numbers": [ 0, 1, 10 ],
        "collatz_report": {"length": 7, "peak": 16},
    }
    assert_exact_match( ganitagya( n ), gold )


def test_2():
    n = 2468
    gold = {
        "even_digits": [ 2, 4, 6, 8 ],
        "is_parity_ordered": True,
        "subset_numbers": [ 
            2, 4, 6, 8, 24, 26, 28, 46,
            48, 68, 246, 248, 268, 468, 2468
         ],
        "collatz_report": {"length": 134, "peak": 9232},
    }
    assert_exact_match( ganitagya( n ), gold )


def test_3():
    n = 97531
    gold = {
        "even_digits": [],
        "is_parity_ordered": True,
        "subset_numbers": [ 
            1, 3, 5, 7, 9, 31, 51, 53,
            71, 73, 75, 91, 93, 95, 97, 531,
            731, 751, 753, 931, 951, 953, 971, 973,
            975, 7531, 9531, 9731, 9751, 9753, 97531
         ],
        "collatz_report": {"length": 297, "peak": 9008980},
    }
    assert_exact_match( ganitagya( n ), gold )


def test_4():
    n = 112
    gold = {
        "even_digits": [ 2 ],
        "is_parity_ordered": False,
        "subset_numbers": [ 1, 2, 11, 12, 112 ],
        "collatz_report": {"length": 21, "peak": 112},
    }
    assert_exact_match( ganitagya( n ), gold )


def test_5():
    n = 27
    gold = {
        "even_digits": [ 2 ],
        "is_parity_ordered": True,
        "subset_numbers": [ 2, 7, 27 ],
        "collatz_report": {"length": 112, "peak": 9232},
    }
    assert_exact_match( ganitagya( n ), gold )
