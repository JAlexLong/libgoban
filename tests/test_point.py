from libgoban import Point


def test_point_1_based_indexing():
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

def test_point_parse():
    pt1_1 = Point(1, 19)
    pt_a1 = Point.parse("a1")
    assert pt1_1 == pt_a1

    pt10_10 = Point(10, 10)
    pt_k10 = Point.parse("k10")
    assert pt10_10 == pt_k10

    pt19_19 = Point(19, 1)
    pt_t19 = Point.parse("t19")
    assert pt19_19 == pt_t19