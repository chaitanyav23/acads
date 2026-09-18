import pytest
from Q2 import jala_chinhit

def assert_exact_match( submitted, gold ):
    assert set( submitted.keys() ) == set( gold.keys() )
    for key in gold:
        assert submitted[ key ] == gold[ key ]

def test_1():
    string = "the good, big fast happy old hot high hard strong bright rich clean cat runs."
    gold = {
        "swappable_count" : 12,
        "naive_signature" : "-000000000000--",
        "naive_watermark" : 0,
        "embed_Deebo_watermark" : "the good, big fast happy old hot high hard sturdy clear wealthy tidy cat runs.",
    }
    assert_exact_match( jala_chinhit( string ), gold )

def test_2():
    string = "the nice large quick glad ancient warm tall tough sturdy clear wealthy tidy cat runs."
    gold = {
        "swappable_count" : 12,
        "naive_signature" : "-111111111111--",
        "naive_watermark" : 4095,
        "embed_Deebo_watermark" : "the good big fast happy old hot high hard sturdy clear wealthy tidy cat runs.",
    }
    assert_exact_match( jala_chinhit( string ), gold )

def test_3():
    string = "a good, bad fast slow happy sad old but new hot cold high low hard easy cat sleeps."
    gold = {
        "swappable_count" : 14,
        "naive_signature" : "-0000000-0000000--",
        "naive_watermark" : 0,
        "embed_Deebo_watermark" : "a good, bad fast slow happy sad old but new hot cool high low tough easy cat sleeps.",
    }
    assert_exact_match( jala_chinhit( string ), gold )

def test_4():
    string = "the good poor. big large fast. sluggish happy unhappy. old ancient hot. warm high tall. hard tough strong. sturdy bright clear. rich wealthy clean. tidy cat runs."
    gold = {
        "swappable_count" : 24,
        "naive_signature" : "-010101010101010101010101--",
        "naive_watermark" : 5592405,
        "embed_Deebo_watermark" : "the good bad. big big fast. slow happy sad. old old hot. hot high high. hard hard strong. strong bright clear. wealthy rich tidy. tidy cat runs.",
    }
    assert_exact_match( jala_chinhit( string ), gold )

def test_5():
    string = "good, bad, fast, slow, happy, sad, old, new, hot, cold, high, low, hard, easy, strong, weak, cat."
    gold = {
        "swappable_count" : 16,
        "naive_signature" : "0000000000000000-",
        "naive_watermark" : 0,
        "embed_Deebo_watermark" : "good, bad, fast, slow, happy, sad, old, new, hot, cold, high, short, hard, easy, strong, frail, cat.",
    }
    assert_exact_match( jala_chinhit( string ), gold )