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
    theta = 90.0
    gold = {
        "single_best": [ 0, 1 ],
        "angle_ids": [ 0, 0, 0, 0, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19 ],
        "directions": [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        "final_heading": 90.0,
    }
    assert_hybrid_match( jodtara_lite( theta ), gold )

def test_2():
    theta = 11.25
    gold = {
        "single_best": [ 1, 1 ],
        "angle_ids": [ 1, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19 ],
        "directions": [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        "final_heading": 11.25,
    }
    assert_hybrid_match( jodtara_lite( theta ), gold )

def test_3():
    theta = 30.0
    gold = {
        "single_best": [ 0, 1 ],
        "angle_ids": [ 0, 2, 4, 6, 8, 10, 12, 14, 16, 17, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19 ],
        "directions": [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        "final_heading": 30.000057220458984,
    }
    assert_hybrid_match( jodtara_lite( theta ), gold )

def test_4():
    theta = -5.625
    gold = {
        "single_best": [ 2, -1 ],
        "angle_ids": [ 2, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19 ],
        "directions": [ -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        "final_heading": -5.625,
    }
    assert_hybrid_match( jodtara_lite( theta ), gold )

def test_5():
    theta = 0.05
    gold = {
        "single_best": [ 9, 1 ],
        "angle_ids": [ 9, 12, 16, 17, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19 ],
        "directions": [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        "final_heading": 0.049953460693359375,
    }
    assert_hybrid_match( jodtara_lite( theta ), gold )