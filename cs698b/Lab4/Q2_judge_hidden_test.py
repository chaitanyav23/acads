import pytest
from Q2 import jala_chinhit

def assert_exact_match( submitted, gold ):
    assert set( submitted.keys() ) == set( gold.keys() )
    for key in gold:
        assert submitted[ key ] == gold[ key ]

def test_1():
    string = "the good big fast happy old hot high hard strong bright rich clean cat runs."
    gold = {
        "swappable_count": 12,
        "naive_signature": "-000000000000--",
        "naive_watermark": 0,
        "embed_Deebo_watermark": "the good big fast happy old hot high hard sturdy clear wealthy tidy cat runs.",
    }
    assert_exact_match( jala_chinhit( string ), gold )

def test_2():
    string = "the good big fast happy old hot high hard strong bright rich clean loud wide deep flat sharp brave cat and dog run fast here today always."
    gold = {
        "swappable_count": 19,
        "naive_signature": "-000000000000000000----0---",
        "naive_watermark": 0,
        "embed_Deebo_watermark": "the good big fast happy old hot high hard strong bright rich clean loud wide steep level sharp bold cat and dog run quick here today always.",
    }
    assert_exact_match( jala_chinhit( string ), gold )

def test_3():
    string = "good bad big small fast slow happy sad old new hot cold high low cat."
    gold = {
        "swappable_count": 14,
        "naive_signature": "00000000000000-",
        "naive_watermark": 0,
        "embed_Deebo_watermark": "good bad big small fast slow happy sad old new warm cool tall short cat.",
    }
    assert_exact_match( jala_chinhit( string ), gold )

def test_4():
    string = "a nice, large quick glad ancient warm tall tough sturdy clear wealthy tidy, brave cat runs."
    gold = {
        "swappable_count": 13,
        "naive_signature": "-1111111111110--",
        "naive_watermark": 8190,
        "embed_Deebo_watermark": "a good, big fast happy old hot high hard sturdy bright rich clean, brave cat runs.",
    }
    assert_exact_match( jala_chinhit( string ), gold )

def test_5():
    string = "good bad big small fast slow happy sad old new hot cold high low hard easy strong weak loud quiet cat sleeps here."
    gold = {
        "swappable_count": 20,
        "naive_signature": "00000000000000000000---",
        "naive_watermark": 0,
        "embed_Deebo_watermark": "good bad big small fast slow happy sad old new hot cold high low hard simple strong frail noisy silent cat sleeps here.",
    }
    assert_exact_match( jala_chinhit( string ), gold )