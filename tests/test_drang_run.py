import pytest
from click import UsageError
from click.testing import CliRunner

from drang_run import __version__, run


def test_version():
    assert __version__ == "0.4.0"


def test_normal_use():
    runner = CliRunner()

    result = runner.invoke(run, args=[])
    assert "Error: Missing argument 'STOP'." in result.output

    result = runner.invoke(run, args=["--help"])
    assert "Usage: run [OPTIONS] [START] STOP [STEP]" in result.output
    assert (
        "Generate a run of integers or characters. Similar to jot and seq."
        in result.output
    )

    # One argument
    result = runner.invoke(run, args=["10"])
    assert "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n" == result.output


@pytest.mark.parametrize("stop", [(10), (20), (40), (100)])
def test_one_arg_pos_int(stop):
    runner = CliRunner()

    # One argument
    result = runner.invoke(run, args=[str(stop)])
    assert "\n".join(str(x) for x in range(1, stop + 1)) + "\n" == result.output


@pytest.mark.parametrize("stop", [(-10), (-20), (-40), (-100)])
@pytest.mark.xfail
def test_one_arg_neg_int(stop):
    runner = CliRunner()

    # One argument
    result = runner.invoke(run, args=[str(stop)])
    assert "\n".join(str(x) for x in range(-1, stop - 1, -1)) + "\n" == result.output


@pytest.mark.parametrize("start,stop", [(5, 10), (10, 20), (1, 40), (99, 100)])
def test_two_arg_pos_int(start, stop):
    runner = CliRunner()

    # One argument
    result = runner.invoke(run, args=[str(start), str(stop)])
    assert "\n".join(str(x) for x in range(start, stop + 1)) + "\n" == result.output


@pytest.mark.parametrize(
    "start,stop", [(0, 10), (5, 10), (10, -20), (-1, 40), (-99, 100), (-10, -50)]
)
def test_two_arg_mixed_int(start, stop):
    runner = CliRunner()

    # One argument
    result = runner.invoke(run, args=[str(start), str(stop)])
    if start > stop:
        gen = range(start, stop - 1, -1)
    else:
        gen = range(start, stop + 1)
    assert "\n".join(str(x) for x in gen) + "\n" == result.output


@pytest.mark.parametrize(
    "start,stop,step",
    [(1, 10, 1), (1, 20, 2), (100, 40, -1), (99, 100, 2), (99, 100, -2)],
)
def test_three_arg_mixed_int(start, stop, step):
    runner = CliRunner()

    # One argument
    result = runner.invoke(run, args=[str(start), str(stop), str(step)])
    if start > stop:
        if step < 0:
            gen = range(start, stop - 1, step)
        else:
            gen = range(start, stop - 1, -1 * step)
    else:
        if step < 0:
            gen = range(start, stop + 1, -1 * step)
        else:
            gen = range(start, stop + 1, step)

    assert "\n".join(str(x) for x in gen) + "\n" == result.output


@pytest.mark.parametrize("start,stop", [(-5, 10), (10, -20), (-1, 40), (-99, 100)])
def test_step_zero(start, stop):
    runner = CliRunner()

    result = runner.invoke(run, args=[str(start), str(stop), "0"])
    assert result != 0
    assert "Error: Invalid value for '[STEP]'" in result.output


@pytest.mark.parametrize(
    "start,stop", [(0, 10), (5, 10), (10, -20), (-1, 40), (-99, 100), (-10, -50)]
)
def test_opt_def(start, stop):
    runner = CliRunner()

    result = runner.invoke(
        run, args=[str(start), str(stop), "--def", "a", "{0}+10", "-f", "{0}+10={a}"]
    )
    assert result != 0

    if start > stop:
        gen = range(start, stop - 1, -1)
    else:
        gen = range(start, stop + 1)
    assert "\n".join(f"{x}+10={x+10}" for x in gen) + "\n" == result.output


def test_opt_def_akku():
    runner = CliRunner()

    expected = [
        6,
        13,
        21,
        30,
        40,
        51,
        63,
        76,
        90,
        97,
        105,
        114,
        124,
        135,
        147,
        160,
        174,
        189,
        197,
        206,
        216,
        227,
        239,
        252,
        266,
        281,
        297,
        306,
        316,
        327,
        339,
        352,
        366,
        381,
        397,
        414,
    ]

    result = runner.invoke(
        run,
        args=[
            "1",
            "4",
            "--also",
            "5",
            "13",
            "1",
            "--def",
            "a",
            "{0}",
            "--def",
            "sum",
            "{a}+{1}",
            "--def",
            "akk",
            "{akk}+{sum}",
            "-f",
            "{akk}",
        ],
    )
    assert result != 0
    assert "\n".join(str(x) for x in expected) + "\n" == result.output
