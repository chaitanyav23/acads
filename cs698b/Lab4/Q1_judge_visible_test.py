import pytest
from Q1 import phalana_bodh

def assert_hybrid_match( submitted, gold ):
    assert set( submitted.keys() ) == set( gold.keys() )
    for key in gold:
        if key == "trapezoid_sum" :
            assert submitted[ key ] == pytest.approx( gold[ key ], abs = 1e-6 )
        if key == "best_linear_fit" :
            assert set( submitted[ key ].keys() ) == set( gold[ key ].keys() )
            for subkey in submitted[ key ]:
                assert submitted[ key ][ subkey ] == pytest.approx( gold[ key ][ subkey ], abs = 1e-6 )
        else:
            assert submitted[ key ] == gold[ key ]

def test_1():
    x = [ 0.0, 1.0, 2.0, 3.0 ]
    y = [ 1.0, 3.0, 5.0, 7.0 ]
    gold = {
        "trapezoid_sum" : 12.0,
        "local_maxima" : [],
        "longest_monotone" : [ ( 0, 4 ) ],
        "best_linear_fit" : {
            "slope" : 2.0,
            "intercept" : 1.0,
        },
    }
    assert_hybrid_match( phalana_bodh( x, y ), gold )

def test_2():
    x = [ -2.0, -1.0, 0.0, 1.0, 2.0 ]
    y = [ -4.0, -1.0, 0.0, -1.0, -4.0 ]
    gold = {
        "trapezoid_sum" : -6.0,
        "local_maxima" : [ 2 ],
        "longest_monotone" : [ ( 0, 3 ), ( 2, 5 ) ],
        "best_linear_fit" : {
            "slope" : 0.0,
            "intercept" : -2.0,
        },
    }
    assert_hybrid_match( phalana_bodh( x, y ), gold )

def test_3():
    x = [ 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0 ]
    y = [ 0.0, 2.0, 0.0, 1.0, 3.0, 1.0, 0.0 ]
    gold = {
        "trapezoid_sum" : 7.0,
        "local_maxima" : [ 1, 4 ],
        "longest_monotone" : [ ( 2, 5 ), ( 4, 7 ) ],
        "best_linear_fit" : {
            "slope" : 0.03571428571428571,
            "intercept" : 0.8928571428571429,
        },
    }
    assert_hybrid_match( phalana_bodh( x, y ), gold )

def test_4():
    x = [ 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0 ]
    y = [ 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0 ]
    gold = {
        "trapezoid_sum" : 3.0,
        "local_maxima" : [ 1, 3, 5 ],
        "longest_monotone" : [ ( 0, 2 ), ( 1, 3 ), ( 2, 4 ), ( 3, 5 ), ( 4, 6 ), ( 5, 7 ) ],
        "best_linear_fit" : {
            "slope" : 0.0,
            "intercept" : 0.42857142857142855,
        },
    }
    assert_hybrid_match( phalana_bodh( x, y ), gold )

def test_5():
    x = [ 0.0, 1.0, 2.0, 3.0, 4.0, 5.0 ]
    y = [ 1.0, 2.0, 2.0, 3.0, 5.0, 4.0 ]
    gold = {
        "trapezoid_sum" : 14.5,
        "local_maxima" : [ 4 ],
        "longest_monotone" : [ ( 2, 5 ) ],
        "best_linear_fit" : {
            "slope" : 0.7142857142857143,
            "intercept" : 1.0476190476190474,
        },
    }
    assert_hybrid_match( phalana_bodh( x, y ), gold )