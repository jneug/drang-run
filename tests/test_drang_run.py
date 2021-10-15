import pytest
from click.testing import CliRunner

from drang_run import __version__, run


def test_version():
    assert __version__ == "0.3.2"


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


@pytest.mark.parametrize("start,stop", [(-5, 10), (10, -20), (-1, 40), (-99, 100)])
def test_two_arg_mixed_int(start, stop):
    runner = CliRunner()

    # One argument
    result = runner.invoke(run, args=[str(start), str(stop)])
    if start > stop:
        gen = range(start, stop - 1, -1)
    else:
        gen = range(start, stop + 1)
    assert "\n".join(str(x) for x in gen) + "\n" == result.output
