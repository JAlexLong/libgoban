# Copyright (C) 2025  J. Alex Long <jalexlong@proton.me>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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


def test_point_from_str():
    pt1_1 = Point(1, 1)
    pt_a1 = Point.from_str("a1")
    assert pt1_1 == pt_a1

    pt8_12 = Point(8, 12)
    pt_h12 = Point.from_str("h12")
    assert pt8_12 == pt_h12

    pt9_11 = Point(9, 11)
    pt_j11 = Point.from_str("j11")
    assert pt9_11 == pt_j11

    pt10_10 = Point(10, 10)
    pt_k10 = Point.from_str("k10")
    assert pt10_10 == pt_k10

    pt19_1 = Point(19, 1)
    pt_t1 = Point.from_str("T1")
    assert pt19_1 == pt_t1

    # covers asymetrical cases
    pt16_9 = Point(16, 9)
    pt_q9 = Point.from_str("q9")
    assert pt16_9 == pt_q9


def test_point_parse_bad_type():
    with pytest.raises(TypeError) as e_info:
        Point.parse()
    
    with pytest.raises(TypeError) as e_info:
        Point.parse(None)
    
    with pytest.raises(TypeError) as e_info:
        Point.parse(13)    


def test_point_parse_invalid_str():
    with pytest.raises(ValueError) as e_info:
        Point.parse('w13')
    
    with pytest.raises(ValueError) as e_info:
        Point.parse('a93')
    
    with pytest.raises(ValueError) as e_info:
        Point.parse('q/11')
    
    with pytest.raises(ValueError) as e_info:
        Point.parse(' f2')
