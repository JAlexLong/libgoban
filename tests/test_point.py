import pytest
from libgoban import Point


def test_point_new():
    # test if class init works as expected with 1-based indexing
    #     and tuple primitives/subclasses
    pt1_1 = Point(1, 1)
    tup1_1 = (1, 1)
    assert pt1_1 == tup1_1

    pt10_10 = Point(10, 10)
    tup10_10 = (10, 10)
    assert pt10_10 == tup10_10

    pt19_19 = Point(19, 19)
    tup19_19 = (19, 19)
    assert pt19_19 == tup19_19

def test_point_new_2():
    # just a little experimental alternate test to test_point_new
    # using a for loop to test *all* points instead
    ...

def test_point_parse():
    pt1_1 = Point(1, 19)
    pt_a1 = Point.parse("a1")
    assert pt1_1 == pt_a1

    pt10_10 = Point(10, 10)
    pt_k10 = Point.parse("k10")
    assert pt10_10 == pt_k10

    pt19_19 = Point(19, 1)
    pt_t19 = Point.parse("T19")
    assert pt19_19 == pt_t19

    # covers asymetrical cases
    pt16_9 = Point(16, 9)
    pt_q11 = Point.parse("q11")
    assert pt16_9 == pt_q11

def test_point_parse_invalid_str():
    with pytest.raises(TypeError) as e_info:
        Point.parse(None)
    
    with pytest.raises(ValueError) as e_info:
        Point.parse('x13')
    
    with pytest.raises(ValueError) as e_info:
        Point.parse('a93')
    
    with pytest.raises(ValueError) as e_info:
        Point.parse('q/11')
    
    with pytest.raises(ValueError) as e_info:
        Point.parse('1-1')
    
    with pytest.raises(ValueError) as e_info:
        Point.parse(' f2')