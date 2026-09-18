import pytest
from Q1 import phalana_bodh

def assert_hybrid_match( submitted, gold ):
    assert set( submitted.keys() ) == set( gold.keys() )
    for key in gold:
        if key == "trapezoid_sum" :
            assert submitted[ key ] == pytest.approx( gold[ key ], abs = 1e-6 )
        if key == "best_linear_fit" :
            assert set( submitted[ key ].keys() ) == set( gold[  key  ].keys() )
            for subkey in submitted[  key  ]:
                assert submitted[ key ][ subkey ] == pytest.approx( gold[ key ][ subkey ], abs = 1e-6 )
        else:
            assert submitted[ key ] == gold[ key ]

def test_1():
    x = [ 0.0, 1.0, 2.0, 3.0, 4.0 ]
    y = [ -2.0, -1.0, 0.0, 2.0, 5.0 ]
    gold = {
        "trapezoid_sum": 2.5,
        "local_maxima": [],
        "longest_monotone": [ ( 0, 5 ) ],
        "best_linear_fit": {
            "slope": 1.7,
            "intercept": -2.6,
        },
    }
    assert_hybrid_match( phalana_bodh( x, y ), gold )

def test_2():
    x = [ 0.0, 1.0, 2.0, 3.0, 4.0 ]
    y = [ 1.0, 2.0, 3.0, 2.0, 1.0 ]
    gold = {
        "trapezoid_sum": 8.0,
        "local_maxima": [ 2 ],
        "longest_monotone": [ ( 0, 3 ), ( 2, 5 ) ],
        "best_linear_fit": {
            "slope": 0.0,
            "intercept": 1.8,
        },
    }
    assert_hybrid_match( phalana_bodh( x, y ), gold )

def test_3():
    x = [ 0.0, 0.5 ]
    y = [ 4.0, 2.0 ]
    gold = {
        "trapezoid_sum": 1.5,
        "local_maxima": [],
        "longest_monotone": [ ( 0, 2 ) ],
        "best_linear_fit": {
            "slope": -4.0,
            "intercept": 4.0,
        },
    }
    assert_hybrid_match( phalana_bodh( x, y ), gold )

def test_4():
    x = [ -3.0, -2.0, -1.0, 0.0, 1.0 ]
    y = [ 2.0, -1.0, 2.0, -1.0, 2.0 ]
    gold = {
        "trapezoid_sum": 2.0,
        "local_maxima": [ 2 ],
        "longest_monotone": [ ( 0, 2 ), ( 1, 3 ), ( 2, 4 ), ( 3, 5 ) ],
        "best_linear_fit": {
            "slope": 0.0,
            "intercept": 0.8,
        },
    }
    assert_hybrid_match( phalana_bodh( x, y ), gold )

def test_5():
    x = [ 0.0, 1.0, 2.0, 3.0 ]
    y = [ 9.0, 6.0, 4.0, 1.0 ]
    gold = {
        "trapezoid_sum": 15.0,
        "local_maxima": [],
        "longest_monotone": [ ( 0, 4 ) ],
        "best_linear_fit": {
            "slope": -2.6,
            "intercept": 8.9,
        },
    }
    assert_hybrid_match( phalana_bodh( x, y ), gold )