import pytest
from Q1 import ganitagya

def assert_exact_match( submitted, gold ):
    assert set( submitted.keys() ) == set( gold.keys() )
    assert submitted == gold

def test_1():
    n = 2831
    gold = {
        "even_digits": [ 2, 8 ],
        "is_parity_ordered": True,
        "subset_numbers": [
            1, 2, 3, 8, 21, 23, 28, 31,
            81, 83, 231, 281, 283, 831, 2831
        ],
        "collatz_report": { "length": 36, "peak": 28672 },
    }
    assert_exact_match( ganitagya( n ), gold )


def test_2():
    n = 123
    gold = {
        "even_digits": [ 2 ],
        "is_parity_ordered": False,
        "subset_numbers": [ 1, 2, 3, 12, 13, 23, 123 ],
        "collatz_report": { "length": 47, "peak": 628 },
    }
    assert_exact_match( ganitagya( n ), gold )


def test_3():
    n = 0
    gold = {
        "even_digits": [ 0 ],
        "is_parity_ordered": True,
        "subset_numbers": [ 0 ],
        "collatz_report": { "length": 1, "peak": 0 },
    }
    assert_exact_match( ganitagya( n ), gold )


def test_4():
    n = 1
    gold = {
        "even_digits": [],
        "is_parity_ordered": True,
        "subset_numbers": [ 1 ],
        "collatz_report": { "length": 1, "peak": 1 },
    }
    assert_exact_match( ganitagya( n ), gold )


def test_5():
    n = 2143
    gold = {
        "even_digits": [ 2, 4 ],
        "is_parity_ordered": False,
        "subset_numbers": [
            1, 2, 3, 4, 13, 14, 21, 23,
            24, 43, 143, 213, 214, 243, 2143
        ],
        "collatz_report": { "length": 170, "peak": 32560 },
    }
    assert_exact_match( ganitagya( n ), gold )
