import pytest
from Q2 import shabd_kala

def assert_exact_match( submitted, gold ):
    assert set( submitted.keys() ) == set( gold.keys() )
    assert submitted == gold

def test_1():
    word = "ZAP"
    gold = {
        "framed": [ "*****", "*ZAP*", "*****" ],
        "diagonal": [ "Z..", ".A.", "..P" ],
        "pyramidal": [ "Z", "ZA", "ZAP" ],
        "anagramal": [ "APZ", "AZP", "PAZ", "PZA", "ZAP", "ZPA" ],
    }
    assert_exact_match( shabd_kala( word ), gold )


def test_2():
    word = "ONE"
    gold = {
        "framed": [ "*****", "*ONE*", "*****" ],
        "diagonal": [ "O..", ".N.", "..E" ],
        "pyramidal": [ "O", "ON", "ONE" ],
        "anagramal": [ "ENO", "EON", "NEO", "NOE", "OEN", "ONE" ],
    }
    assert_exact_match( shabd_kala( word ), gold )


def test_3():
    word = "MIX"
    gold = {
        "framed": [ "*****", "*MIX*", "*****" ],
        "diagonal": [ "M..", ".I.", "..X" ],
        "pyramidal": [ "M", "MI", "MIX" ],
        "anagramal": [ "IMX", "IXM", "MIX", "MXI", "XIM", "XMI" ],
    }
    assert_exact_match( shabd_kala( word ), gold )


def test_4():
    word = "BAT"
    gold = {
        "framed": [ "*****", "*BAT*", "*****" ],
        "diagonal": [ "B..", ".A.", "..T" ],
        "pyramidal": [ "B", "BA", "BAT" ],
        "anagramal": [ "ABT", "ATB", "BAT", "BTA", "TAB", "TBA" ],
    }
    assert_exact_match( shabd_kala( word ), gold )


def test_5():
    
    word = "YES"
    gold = {
        "framed": [ "*****", "*YES*", "*****" ],
        "diagonal": [ "Y..", ".E.", "..S" ],
        "pyramidal": [ "Y", "YE", "YES" ],
        "anagramal": [ "ESY", "EYS", "SEY", "SYE", "YES", "YSE" ],
    }
    assert_exact_match( shabd_kala( word ), gold )
