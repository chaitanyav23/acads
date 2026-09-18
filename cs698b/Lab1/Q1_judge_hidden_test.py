import pytest
from Q1 import megha_summary

def assert_hybrid_match( submitted, gold ):
    assert set( submitted.keys() ) == set( gold.keys() )
    for key in gold:
        if key == "total" or key == "average" :
            assert submitted[ key ] == pytest.approx( gold[ key ], abs = 1e-6 )
        else:
            assert submitted[ key ] == gold[ key ]

def test_1():
    rainfall_list = [ 3, 5, 5, 1 ]
    gold = {
        "total": 14,
        "average": 3.5,
        "rainy_days": 4,
        "rainiest_day": 2,
        "longest_drought": 0,
    }
    assert_hybrid_match( megha_summary( rainfall_list ), gold )


def test_2():
    rainfall_list = [ 1, 0, 0 ]
    gold = {
        "total": 1,
        "average": 0.3333333333333333,
        "rainy_days": 1,
        "rainiest_day": 1,
        "longest_drought": 2,
    }
    assert_hybrid_match( megha_summary( rainfall_list ), gold )


def test_3():
    rainfall_list = [ 0, 0, 1, 0, 0, 0, 2 ]
    gold = {
        "total": 3,
        "average": 0.42857142857142855,
        "rainy_days": 2,
        "rainiest_day": 7,
        "longest_drought": 3,
    }
    assert_hybrid_match( megha_summary( rainfall_list ), gold )


def test_4():
    rainfall_list = [ 0 ]
    gold = {
        "total": 0,
        "average": 0,
        "rainy_days": 0,
        "rainiest_day": 1,
        "longest_drought": 1,
    }
    assert_hybrid_match( megha_summary( rainfall_list ), gold )


def test_5():
    rainfall_list = [ 0, 1.5, 0, 1.5, 0 ]
    gold = {
        "total": 3.0,
        "average": 0.6,
        "rainy_days": 2,
        "rainiest_day": 2,
        "longest_drought": 1,
    }
    assert_hybrid_match( megha_summary( rainfall_list ), gold )
