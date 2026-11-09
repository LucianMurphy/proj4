import arrow
from nose.tools import assert_equal, raises
from acp_times import open_time, close_time

START ="2017-01-01T00:00:00+00:00"

def at(hours, minutes):
    return arrow.get(START).shift(hours = hours, minutes = minutes).isoformat()

def test_start():
    assert_equal(open_time(0, 200, START), at(0, 0))
    assert_equal(close_time(0, 200, START), at(1, 0))

def test_single_dist():
    assert_equal(open_time(100, 200, START), at(2, 56))
    assert_equal(close_time(100, 200, START), at(6, 40))

def test_early_control():
    assert_equal(close_time(40, 200, START), at(3, 0))
    assert_equal(close_time(60, 200, START), at(4, 0))
    assert_equal(open_time(60, 200, START), at(1, 46))

def test_multiple_dists_open():
    assert_equal(open_time(350, 600, START), at(10, 34))
    assert_equal(close_time(350, 600, START), at(23, 20))

def test_long_brevet():
    assert_equal(open_time(890, 1000, START), at(29, 9))
    assert_equal(close_time(890, 1000, START), at(65, 23))

def test_finish_fixed_close_times():
    assert_equal(close_time(200, 200, START), at(13, 30))
    assert_equal(close_time(400, 400, START), at(27, 0))
    assert_equal(close_time(1000, 1000, START), at(75, 0))

def test_control_past_finish():
    assert_equal(open_time(205, 200, START), open_time(200, 200, START))
    assert_equal(close_time(205, 200, START), at(13, 30))

@raises(ValueError)
def test_invalid_brevet_distance():
    open_time(100, 250, START)
 
 
@raises(ValueError)
def test_control_too_far_past_finish():
    close_time(300, 200, START)