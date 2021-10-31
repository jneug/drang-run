import pytest

from drang_run import Counter


def sign(n):
    return (n > 0) - (n < 0)


@pytest.mark.parametrize(
    "start,stop,step",
    [
        (1, 10, 1),
        (1, 20, 2),
        (1, 20, 3),
        (100, 40, -1),
        (0, 10, 2),
        (5, 10, 1),
        (10, -20, -1),
        (-1, 40, 1),
        (-99, 100, 1),
        (-10, -50, -1),
        (99, 100, 1),
    ],
)
def test_counter(start, stop, step):
    expected = range(start, stop + sign(step), step)

    cnt = Counter(start, stop, step)
    assert list(cnt) == list(expected)

    cnt_rev = Counter(start, stop, step, True)
    assert list(cnt_rev) == list(reversed(expected))


@pytest.mark.parametrize(
    "start,stop,step",
    [
        (1, 1, 1),
        (1, 1, 2),
        (1, 1, -1),
        (0, 0, 1),
        (0, 0, 10),
        (0, 0, -10),
        (100, 100, 1),
        (100, 100, 2),
        (100, 100, -1),
        (-100, -100, -1),
        (-100, -100, -2),
        (-100, -100, 1),
    ],
)
def test_counter_start_eq_stop(start, stop, step):
    assert start == stop

    cnt = Counter(start, stop, step)
    assert list(cnt) == [start]

    cnt_rev = Counter(start, stop, step, True)
    assert list(cnt_rev) == [start]


@pytest.mark.parametrize(
    "start,stop,step",
    [(99, 100, 2), (100, 99, -2), (0, 5, 10), (1, 10, 100), (500, 0, -1000)],
)
def test_counter_step_gt_diff(start, stop, step):
    expected = range(start, stop + sign(step), step)
    assert len(expected) == 1

    cnt = Counter(start, stop, step)
    assert list(cnt) == list(expected)


@pytest.mark.parametrize(
    "start,stop,step,expected",
    [
        (1, 10, -1, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        (10, 1, 1, [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]),
        (-5, 5, -1, [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]),
        (5, -5, 1, [5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5]),
    ],
)
def test_counter_wrong_step(start, stop, step, expected):
    cnt = Counter(start, stop, step)
    assert list(cnt) == expected


def test_counter_step_zero():
    with pytest.raises(ValueError):
        Counter(1, 100, 0)

    with pytest.raises(ValueError):
        Counter(-10, 10, 0)
