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
    sx, sy = 0.38268343236508984, 0.9238795325112867
    gold = {
        "single_best": [ 0, 1 ],
        "angle_ids": [ 0, 0, 0, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19 ],
        "directions": [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        "final_heading": [ 0.38268343236508967, 0.9238795325112867 ],
    }
    assert_hybrid_match( jodtara( sx, sy ), gold )

def test_2():
    sx, sy = 0.6691306063588582, 0.7431448254773942
    gold = {
        "single_best": [ 0, 1 ],
        "angle_ids": [ 0, 0, 3, 7, 11, 15, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19 ],
        "directions": [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        "final_heading": [ 0.6691312000929598, 0.7431442908763788 ],
    }
    assert_hybrid_match( jodtara( sx, sy ), gold )

def test_3():
    sx, sy = 0.9238795325112867, 0.3826834323650898
    gold = {
        "single_best": [ 0, 1 ],
        "angle_ids": [ 0, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19 ],
        "directions": [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        "final_heading": [ 0.9238795325112867, 0.3826834323650898 ],
    }
    assert_hybrid_match( jodtara( sx, sy ), gold )

def test_4():
    sx, sy = 0.7071067811865476, -0.7071067811865476
    gold = {
        "single_best": [ 0, -1 ],
        "angle_ids": [ 0, 0, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19 ],
        "directions": [ -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        "final_heading": [ 0.7071067811865475, -0.7071067811865476 ],
    }
    assert_hybrid_match( jodtara( sx, sy ), gold )

def test_5():
    sx, sy = 0.9659258262890683, 0.25881904510252074
    gold = {
        "single_best": [ 1, 1 ],
        "angle_ids": [ 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19 ],
        "directions": [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        "final_heading": [ 0.9659260847673903, 0.25881808044636306 ],
    }
    assert_hybrid_match( jodtara( sx, sy ), gold )