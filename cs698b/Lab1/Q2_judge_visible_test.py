import pytest
from Q2 import shabd_kala

def assert_exact_match( submitted, gold ):
    assert set( submitted.keys() ) == set( gold.keys() )
    assert submitted == gold

def test_1():
    word = "CAT"
    gold = {
        "framed": [ "*****", "*CAT*", "*****" ],
        "diagonal": [ "C..", ".A.", "..T" ],
        "pyramidal": [ "C", "CA", "CAT" ],
        "anagramal": [ "ACT", "ATC", "CAT", "CTA", "TAC", "TCA" ],
    }
    assert_exact_match( shabd_kala( word ), gold )


def test_2():
    word = "DOG"
    gold = {
        "framed": [ "*****", "*DOG*", "*****" ],
        "diagonal": [ "D..", ".O.", "..G" ],
        "pyramidal": [ "D", "DO", "DOG" ],
        "anagramal": [ "DGO", "DOG", "GDO", "GOD", "ODG", "OGD" ],
    }
    assert_exact_match( shabd_kala( word ), gold )


def test_3():
    word = "FUN"
    gold = {
        "framed": [ "*****", "*FUN*", "*****" ],
        "diagonal": [ "F..", ".U.", "..N" ],
        "pyramidal": [ "F", "FU", "FUN" ],
        "anagramal": [ "FNU", "FUN", "NFU", "NUF", "UFN", "UNF" ],
    }
    assert_exact_match( shabd_kala( word ), gold )


def test_4():
    word = "SKY"
    gold = {
        "framed": [ "*****", "*SKY*", "*****" ],
        "diagonal": [ "S..", ".K.", "..Y" ],
        "pyramidal": [ "S", "SK", "SKY" ],
        "anagramal": [ "KSY", "KYS", "SKY", "SYK", "YKS", "YSK" ],
    }
    assert_exact_match( shabd_kala( word ), gold )


def test_5():
    word = "RED"
    gold = {
        "framed": [ "*****", "*RED*", "*****" ],
        "diagonal": [ "R..", ".E.", "..D" ],
        "pyramidal": [ "R", "RE", "RED" ],
        "anagramal": [ "DER", "DRE", "EDR", "ERD", "RDE", "RED" ],
    }
    assert_exact_match( shabd_kala( word ), gold )
