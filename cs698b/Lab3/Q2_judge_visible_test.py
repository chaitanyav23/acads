import pytest
from Q2 import varnamala

def assert_exact_match( submitted, gold ):
    assert set( submitted.keys() ) == set( gold.keys() )
    for key in gold:
        assert submitted[ key ] == gold[ key ]

def test_1():
    string = "ab ca"
    gold = {
        "frequencies" : {
            'a' : 2, 'b' : 1, 'c' : 1, 'd' : 0, 'e' : 0, 'f' : 0, 'g' : 0,
            'h' : 0, 'i' : 0, 'j' : 0, 'k' : 0, 'l' : 0, 'm' : 0, 'n' : 0,
            'o' : 0, 'p' : 0, 'q' : 0, 'r' : 0, 's' : 0, 't' : 0, 'u' : 0,
            'v' : 0, 'w' : 0, 'x' : 0, 'y' : 0, 'z' : 0
        },
        "neighbor_map" : {
            'a' : { 'b' },
            'b' : { None },
            'c' : { 'a' },
            'd' : set(),
            'e' : set(),
            'f' : set(),
            'g' : set(),
            'h' : set(),
            'i' : set(),
            'j' : set(),
            'k' : set(),
            'l' : set(),
            'm' : set(),
            'n' : set(),
            'o' : set(),
            'p' : set(),
            'q' : set(),
            'r' : set(),
            's' : set(),
            't' : set(),
            'u' : set(),
            'v' : set(),
            'w' : set(),
            'x' : set(),
            'y' : set(),
            'z' : set()
        },
        "longest_echo" : [ "a" ],
        "signature" : "abc",
    }
    assert_exact_match( varnamala( string ), gold )


def test_2():
    string = "cab"
    gold = {
        "frequencies" : {
            'a' : 1, 'b' : 1, 'c' : 1, 'd' : 0, 'e' : 0, 'f' : 0, 'g' : 0,
            'h' : 0, 'i' : 0, 'j' : 0, 'k' : 0, 'l' : 0, 'm' : 0, 'n' : 0,
            'o' : 0, 'p' : 0, 'q' : 0, 'r' : 0, 's' : 0, 't' : 0, 'u' : 0,
            'v' : 0, 'w' : 0, 'x' : 0, 'y' : 0, 'z' : 0
        },
        "neighbor_map" : {
            'a' : { 'b' },
            'b' : { None },
            'c' : { 'a' },
            'd' : set(),
            'e' : set(),
            'f' : set(),
            'g' : set(),
            'h' : set(),
            'i' : set(),
            'j' : set(),
            'k' : set(),
            'l' : set(),
            'm' : set(),
            'n' : set(),
            'o' : set(),
            'p' : set(),
            'q' : set(),
            'r' : set(),
            's' : set(),
            't' : set(),
            'u' : set(),
            'v' : set(),
            'w' : set(),
            'x' : set(),
            'y' : set(),
            'z' : set()
        },
        "longest_echo" : [],
        "signature" : "cab",
    }
    assert_exact_match( varnamala( string ), gold )


def test_3():
    string = "aaaa"
    gold = {
        "frequencies" : {
            'a' : 4, 'b' : 0, 'c' : 0, 'd' : 0, 'e' : 0, 'f' : 0, 'g' : 0,
            'h' : 0, 'i' : 0, 'j' : 0, 'k' : 0, 'l' : 0, 'm' : 0, 'n' : 0,
            'o' : 0, 'p' : 0, 'q' : 0, 'r' : 0, 's' : 0, 't' : 0, 'u' : 0,
            'v' : 0, 'w' : 0, 'x' : 0, 'y' : 0, 'z' : 0
        },
        "neighbor_map" : {
            'a' : { 'a' },
            'b' : set(),
            'c' : set(),
            'd' : set(),
            'e' : set(),
            'f' : set(),
            'g' : set(),
            'h' : set(),
            'i' : set(),
            'j' : set(),
            'k' : set(),
            'l' : set(),
            'm' : set(),
            'n' : set(),
            'o' : set(),
            'p' : set(),
            'q' : set(),
            'r' : set(),
            's' : set(),
            't' : set(),
            'u' : set(),
            'v' : set(),
            'w' : set(),
            'x' : set(),
            'y' : set(),
            'z' : set()
        },
        "longest_echo" : [ "aaa" ],
        "signature" : "a",
    }
    assert_exact_match( varnamala( string ), gold )


def test_4():
    string = "bananas"
    gold = {
        "frequencies" : {
            'a' : 3, 'b' : 1, 'c' : 0, 'd' : 0, 'e' : 0, 'f' : 0, 'g' : 0,
            'h' : 0, 'i' : 0, 'j' : 0, 'k' : 0, 'l' : 0, 'm' : 0, 'n' : 2,
            'o' : 0, 'p' : 0, 'q' : 0, 'r' : 0, 's' : 1, 't' : 0, 'u' : 0,
            'v' : 0, 'w' : 0, 'x' : 0, 'y' : 0, 'z' : 0
        },
        "neighbor_map" : {
            'a' : { 'n', 's' },
            'b' : { 'a' },
            'c' : set(),
            'd' : set(),
            'e' : set(),
            'f' : set(),
            'g' : set(),
            'h' : set(),
            'i' : set(),
            'j' : set(),
            'k' : set(),
            'l' : set(),
            'm' : set(),
            'n' : { 'a' },
            'o' : set(),
            'p' : set(),
            'q' : set(),
            'r' : set(),
            's' : { None },
            't' : set(),
            'u' : set(),
            'v' : set(),
            'w' : set(),
            'x' : set(),
            'y' : set(),
            'z' : set()
        },
        "longest_echo" : [ "ana" ],
        "signature" : "anbs",
    }
    assert_exact_match( varnamala( string ), gold )


def test_5():
    string = "a b a"
    gold = {
        "frequencies" : {
            'a' : 2, 'b' : 1, 'c' : 0, 'd' : 0, 'e' : 0, 'f' : 0, 'g' : 0,
            'h' : 0, 'i' : 0, 'j' : 0, 'k' : 0, 'l' : 0, 'm' : 0, 'n' : 0,
            'o' : 0, 'p' : 0, 'q' : 0, 'r' : 0, 's' : 0, 't' : 0, 'u' : 0,
            'v' : 0, 'w' : 0, 'x' : 0, 'y' : 0, 'z' : 0
        },
        "neighbor_map" : {
            'a' : { None },
            'b' : { None },
            'c' : set(),
            'd' : set(),
            'e' : set(),
            'f' : set(),
            'g' : set(),
            'h' : set(),
            'i' : set(),
            'j' : set(),
            'k' : set(),
            'l' : set(),
            'm' : set(),
            'n' : set(),
            'o' : set(),
            'p' : set(),
            'q' : set(),
            'r' : set(),
            's' : set(),
            't' : set(),
            'u' : set(),
            'v' : set(),
            'w' : set(),
            'x' : set(),
            'y' : set(),
            'z' : set()
        },
        "longest_echo" : [ " ", "a" ],
        "signature" : "ab",
    }
    assert_exact_match( varnamala( string ), gold )
