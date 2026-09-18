import pytest
from Q2 import jodtara

def assert_hybrid_match( submitted, gold ):
    assert set( submitted.keys() ) == set( gold.keys() )
    for key in gold:
        if key == "final_heading":
            assert submitted[ key ][ 0 ] == pytest.approx( gold[ key ][ 0 ], abs = 1e-6 )
            assert submitted[ key ][ 1 ] == pytest.approx( gold[ key ][ 1 ], abs = 1e-6 )
        else:
            assert submitted[ key ] == gold[ key ]

def test_1():
    sx, sy = 0.0, 1.0
    gold = {
        "single_best": [ 0, 1 ],
        "angle_ids": [ 0, 0, 0, 0, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19 ],
        "directions": [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        "final_heading": [ -1.1102230246251565e-16, 1.0 ],
    }
    assert_hybrid_match( jodtara( sx, sy ), gold )

def test_2():
    sx, sy = 0.9807852804032304, 0.19509032201612825
    gold = {
        "single_best": [ 1, 1 ],
        "angle_ids": [ 1, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19 ],
        "directions": [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        "final_heading": [ 0.9807852804032304, 0.19509032201612825 ],
    }
    assert_hybrid_match( jodtara( sx, sy ), gold )

def test_3():
    sx, sy = 0.7071067811865476, 0.7071067811865476
    gold = {
        "single_best": [ 0, 1 ],
        "angle_ids": [ 0, 0, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19 ],
        "directions": [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        "final_heading": [ 0.7071067811865475, 0.7071067811865476 ],
    }
    assert_hybrid_match( jodtara( sx, sy ), gold )

def test_4():
    sx, sy = 0.9951847266721969, -0.0980171403295606
    gold = {
        "single_best": [ 2, -1 ],
        "angle_ids": [ 2, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19 ],
        "directions": [ -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        "final_heading": [ 0.9951847266721969, -0.0980171403295606 ],
    }
    assert_hybrid_match( jodtara( sx, sy ), gold )

def test_5():
    sx, sy = 0.8660254037844387, 0.49999999999999994
    gold = {
        "single_best": [ 0, 1 ],
        "angle_ids": [ 0, 2, 4, 6, 8, 10, 12, 14, 16, 17, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19 ],
        "directions": [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        "final_heading": [ 0.8660249044413022, 0.500000864886685 ],
    }
    assert_hybrid_match( jodtara( sx, sy ), gold )