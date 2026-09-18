import pytest
from Q1 import jodtara_lite
from lookup import DEG_TOL

def assert_hybrid_match( submitted, gold ):
    assert set( submitted.keys() ) == set( gold.keys() )
    for key in gold:
        if key == "final_heading":
            assert submitted[ key ] == pytest.approx( gold[ key ], abs = DEG_TOL )
        else:
            assert submitted[ key ] == gold[ key ]

def test_1():
    theta = -67.5
    gold = {
        "single_best": [ 0, -1 ],
        "angle_ids": [ 0, 0, 0, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19 ],
        "directions": [ -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        "final_heading": -67.5,
    }
    assert_hybrid_match( jodtara_lite( theta ), gold )

def test_2():
    theta = 48.0
    gold = {
        "single_best": [ 0, 1 ],
        "angle_ids": [ 0, 0, 3, 7, 11, 15, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19 ],
        "directions": [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        "final_heading": 47.99995422363281,
    }
    assert_hybrid_match( jodtara_lite( theta ), gold )

def test_3():
    theta = -80.0
    gold = {
        "single_best": [ 0, -1 ],
        "angle_ids": [ 0, 0, 0, 1, 4, 7, 10, 13, 16, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19 ],
        "directions": [ -1, -1, -1, -1, -1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        "final_heading": -80.00003814697266,
    }
    assert_hybrid_match( jodtara_lite( theta ), gold )

def test_4():
    theta = 15.0
    gold = {
        "single_best": [ 1, 1 ],
        "angle_ids": [ 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19 ],
        "directions": [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        "final_heading": 14.999942779541016,
    }
    assert_hybrid_match( jodtara_lite( theta ), gold )

def test_5():
    theta = 7.0
    gold = {
        "single_best": [ 2, 1 ],
        "angle_ids": [ 2, 4, 10, 11, 14, 16, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19 ],
        "directions": [ 1, 1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        "final_heading": 7.000007629394531,
    }
    assert_hybrid_match( jodtara_lite( theta ), gold )