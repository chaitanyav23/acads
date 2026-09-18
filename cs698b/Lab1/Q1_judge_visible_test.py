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
    rainfall_list = [ 0, 2.5, 0, 0, 0, 1.0, 4.5 ]
    gold = {
        "total" : 8.0,
        "average" : 1.1428571428571428,
        "rainy_days" : 3,
        "rainiest_day" : 7,
        "longest_drought" : 3,
    }
    assert_hybrid_match( megha_summary( rainfall_list ), gold )


def test_2():
    rainfall_list = []
    gold = {
        "total" : 0,
        "average" : 0,
        "rainy_days" : 0,
        "rainiest_day" : None,
        "longest_drought" : 0,
    }
    assert_hybrid_match( megha_summary( rainfall_list ), gold )


def test_3():
    rainfall_list = [ 0, 0, 0, 0 ]
    gold = {
        "total" : 0,
        "average" : 0.0,
        "rainy_days" : 0,
        "rainiest_day" : 1,
        "longest_drought" : 4,
    }
    assert_hybrid_match( megha_summary( rainfall_list ), gold )


def test_4():
    rainfall_list = [ 5 ]
    gold = {
        "total" : 5,
        "average" : 5.0,
        "rainy_days" : 1,
        "rainiest_day" : 1,
        "longest_drought" : 0,
    }
    assert_hybrid_match( megha_summary( rainfall_list ), gold )


def test_5():
    rainfall_list = [ 1.0, 2.0, 3.0 ]
    gold = {
        "total" : 6.0,
        "average" : 2.0,
        "rainy_days" : 3,
        "rainiest_day" : 3,
        "longest_drought" : 0,
    }
    assert_hybrid_match( megha_summary( rainfall_list ), gold )
