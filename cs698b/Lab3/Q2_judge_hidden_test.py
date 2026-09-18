import pytest
from Q2 import varnamala

def assert_exact_match( submitted, gold ):
    assert set( submitted.keys() ) == set( gold.keys() )
    for key in gold:
        assert submitted[ key ] == gold[ key ]

def test_1():
    string = 'aa a'
    gold = {
        "frequencies": {
            'a': 3, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0,
            'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0,
            'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0,
            'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0
        },
        "neighbor_map": {
            'a': {'a'},
            'b': set(),
            'c': set(),
            'd': set(),
            'e': set(),
            'f': set(),
            'g': set(),
            'h': set(),
            'i': set(),
            'j': set(),
            'k': set(),
            'l': set(),
            'm': set(),
            'n': set(),
            'o': set(),
            'p': set(),
            'q': set(),
            'r': set(),
            's': set(),
            't': set(),
            'u': set(),
            'v': set(),
            'w': set(),
            'x': set(),
            'y': set(),
            'z': set()
        },
        "longest_echo": [ 'a' ],
        "signature": 'a',
    }
    assert_exact_match( varnamala( string ), gold )


def test_2():
    string = 'abba'
    gold = {
        "frequencies": {
            'a': 2, 'b': 2, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0,
            'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0,
            'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0,
            'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0
        },
        "neighbor_map": {
            'a': {'b'},
            'b': {'a', 'b'},
            'c': set(),
            'd': set(),
            'e': set(),
            'f': set(),
            'g': set(),
            'h': set(),
            'i': set(),
            'j': set(),
            'k': set(),
            'l': set(),
            'm': set(),
            'n': set(),
            'o': set(),
            'p': set(),
            'q': set(),
            'r': set(),
            's': set(),
            't': set(),
            'u': set(),
            'v': set(),
            'w': set(),
            'x': set(),
            'y': set(),
            'z': set()
        },
        "longest_echo": [ 'a', 'b' ],
        "signature": 'ab',
    }
    assert_exact_match( varnamala( string ), gold )


def test_3():
    string = 'the cat sat'
    gold = {
        "frequencies": {
            'a': 2, 'b': 0, 'c': 1, 'd': 0, 'e': 1, 'f': 0, 'g': 0,
            'h': 1, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0,
            'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 1, 't': 3, 'u': 0,
            'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0
        },
        "neighbor_map": {
            'a': {'t'},
            'b': set(),
            'c': {'a'},
            'd': set(),
            'e': {None},
            'f': set(),
            'g': set(),
            'h': {'e'},
            'i': set(),
            'j': set(),
            'k': set(),
            'l': set(),
            'm': set(),
            'n': set(),
            'o': set(),
            'p': set(),
            'q': set(),
            'r': set(),
            's': {'a'},
            't': {'h'},
            'u': set(),
            'v': set(),
            'w': set(),
            'x': set(),
            'y': set(),
            'z': set()
        },
        "longest_echo": [ 'at' ],
        "signature": 'tahecs',
    }
    assert_exact_match( varnamala( string ), gold )


def test_4():
    string = 'mississippi'
    gold = {
        "frequencies": {
            'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0,
            'h': 0, 'i': 4, 'j': 0, 'k': 0, 'l': 0, 'm': 1, 'n': 0,
            'o': 0, 'p': 2, 'q': 0, 'r': 0, 's': 4, 't': 0, 'u': 0,
            'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0
        },
        "neighbor_map": {
            'a': set(),
            'b': set(),
            'c': set(),
            'd': set(),
            'e': set(),
            'f': set(),
            'g': set(),
            'h': set(),
            'i': {'p', 's'},
            'j': set(),
            'k': set(),
            'l': set(),
            'm': {'i'},
            'n': set(),
            'o': set(),
            'p': {'i', 'p'},
            'q': set(),
            'r': set(),
            's': {'i', 's'},
            't': set(),
            'u': set(),
            'v': set(),
            'w': set(),
            'x': set(),
            'y': set(),
            'z': set()
        },
        "longest_echo": [ 'issi' ],
        "signature": 'ispm',
    }
    assert_exact_match( varnamala( string ), gold )


def test_5():
    string = 'ab cd'
    gold = {
        "frequencies": {
            'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 0, 'f': 0, 'g': 0,
            'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0,
            'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0,
            'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0
        },
        "neighbor_map": {
            'a': {'b'},
            'b': {None},
            'c': {'d'},
            'd': {None},
            'e': set(),
            'f': set(),
            'g': set(),
            'h': set(),
            'i': set(),
            'j': set(),
            'k': set(),
            'l': set(),
            'm': set(),
            'n': set(),
            'o': set(),
            'p': set(),
            'q': set(),
            'r': set(),
            's': set(),
            't': set(),
            'u': set(),
            'v': set(),
            'w': set(),
            'x': set(),
            'y': set(),
            'z': set()
        },
        "longest_echo": [],
        "signature": 'abcd',
    }
    assert_exact_match( varnamala( string ), gold )
