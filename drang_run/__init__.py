# -*- coding: utf-8 -*-

__version__ = "0.4.1"


import codecs
import decimal
import ast
import operator
from itertools import product
from math import sqrt
from string import ascii_letters

import click

import drang_run.simpleeval as simpleeval


# The arguments for -f and -s come in as raw strings, but we
# need to be able to interpret things like \t and \n as escape
# sequences, not literals.
def interpret(s):
    if s:
        return codecs.escape_decode(bytes(s, "utf8"))[0].decode("utf8")
    else:
        return None


class Counter(object):
    """
    Counter class to create the range for a given counter. Either the "main" counter
    or an "--also" counter. The counter decides how to count (chars, ints or floats)
    based on the values of start, stop and step.
    """

    def __init__(self, start, stop, step, reverse=False):
        if str(start) in ascii_letters or str(stop) in ascii_letters:
            if start not in ascii_letters:
                raise ValueError(
                    f"For character counters 'START' needs to be a character. Given: {start}"
                )
            if stop not in ascii_letters:
                raise ValueError(
                    f"For character counters 'STOP' needs to be a character. Given: {stop}"
                )
            self.start = ord(start)
            self.stop = ord(stop)
            self.type = chr
        else:
            try:
                self.start = decimal.Decimal(start)
            except decimal.InvalidOperation:
                raise ValueError(
                    f"Invalid value for '[START]': '{start}' is not a valid number."
                )
            try:
                self.stop = decimal.Decimal(stop)
            except decimal.InvalidOperation:
                raise ValueError(
                    f"Invalid value for 'STOP': '{stop}' is not a valid number."
                )

            if "." in str(start) or "." in str(stop) or "." in str(step):
                self.type = float
            else:
                self.type = int

        try:
            self.step = abs(decimal.Decimal(step))
        except decimal.InvalidOperation:
            raise ValueError(
                f"Invalid value for '[STEP]': '{step}' is not a valid number."
            )

        if self.step == 0.0:
            raise ValueError("Invalid value for '[STEP]': Step size may not be zero.")

        self.reversed = False  # reverse
        if self.start > self.stop:
            # self.start, self.stop = self.stop, self.start
            self.step = -1 * self.step
            self.reversed = not self.reversed

        if reverse:
            self.start, self.stop = self.stop, self.start
            self.step = -1 * self.step
            self.reversed = not self.reversed

    def __iter__(self):
        num = self.start
        while (not self.reversed and num <= self.stop) or (
            self.reversed and num >= self.stop
        ):
            yield self.type(num)
            num += self.step


class OptargCommand(click.Command):
    """Custom command to make the first argument optional.
    If only one argument is given, the default value for START
    is prepended to the argument list."""

    def parse_args(self, ctx, args):
        # preparse args to check if STOP was given
        parser = super(OptargCommand, self).make_parser(ctx)
        parsed, _, _ = parser.parse_args(args.copy())
        # Only START is set, prepend the default for START
        if not parsed["stop"]:
            start_arg = next(
                a for a in ctx.command.params if a.human_readable_name == "START"
            )
            args.insert(0, start_arg.default)
        super(OptargCommand, self).parse_args(ctx, args)


@click.command(cls=OptargCommand, context_settings={"ignore_unknown_options": True})
@click.version_option(version=__version__, prog_name="run")
@click.option("-f", "--format", "fstring", help="formatting string for number")
@click.option("-s", "--sep", help="separator string", default="\n")
@click.option("-r", "--reverse", is_flag=True)
@click.option(
    "--also",
    multiple=True,
    nargs=3,
    help="Also run another counter with start, stop and step settings. "
    "All three need to be present.",
    metavar="START STOP STEP",
)
@click.option(
    "-d",
    "--def",
    "var_defs",
    multiple=True,
    nargs=2,
    help="Define a variable to use in the format string. The Variable may contain simple arithmetic expressions.",
    metavar="NAME EXPR",
)
@click.argument("start", required=False, default="1")
@click.argument("stop")
@click.argument("step", required=False, default="1")
@click.pass_context
def run(ctx, start, stop, step, fstring, sep, reverse, also, var_defs):
    """Generate a run of integers or characters. Similar to jot and seq.

    The run of numbers can be integers or reals, depending on the values of START, STOP, and STEP.
    The defaults for both START and STEP are 1. If both START and STOP are characters and STEP is an
    integer, the result will be characters."""
    fstring = interpret(fstring) or "-".join(["{}"] * (len(also) + 1))
    sep = interpret(sep) or "\n"

    try:
        counters = [Counter(start, stop, step, reverse=reverse)]
    except ValueError as err:
        ctx.fail(str(err))

    if also:
        for counter in also:
            try:
                counters.append(Counter(*counter, reverse=reverse))
            except ValueError as err:
                ctx.fail(str(err))

    # Initialize variable defintions
    variables = {name: 0 for name, ex in var_defs}

    # Lazy evaluation of counter product
    # Each iteration is printed directly after evaluation.
    # itertools.product still takes a moment to build the cartesian
    # product of counter values for large inputs.

    # Create restricted evaluator singleton
    simple = simpleeval.SimpleEval()
    simple.functions.update(sqrt=sqrt)
    simple.operators[ast.BitOr] = operator.or_
    simple.operators[ast.BitAnd] = operator.and_
    simple.operators[ast.BitXor] = operator.xor

    is_first = True
    for numbers in product(*counters):
        try:
            # Evaluate expressions in variable definitions
            # for this instance of the counters
            for name, expression in var_defs:
                for i, v in enumerate(numbers):
                    expression = expression.replace(f"{{{i}}}", str(v))
                for n, v in variables.items():
                    expression = expression.replace(f"{{{n}}}", str(v))
                variables[name] = simple.eval(expression)
        except (
            simpleeval.InvalidExpression,
            simpleeval.FunctionNotDefined,
            simpleeval.NameNotDefined,
            simpleeval.AttributeDoesNotExist,
            simpleeval.FeatureNotAvailable,
            simpleeval.NumberTooHigh,
            simpleeval.IterableTooLong,
        ) as err:
            format_opt = next(
                a for a in ctx.command.params if a.human_readable_name == "var_defs"
            )
            hint = format_opt.get_error_hint(ctx)
            ctx.fail(f"Invalid value for {hint}: {str(err)}")

        try:
            # Convert iteration to text, using the provided format string
            if not is_first:
                click.echo(sep, nl=False)
            else:
                is_first = False
            click.echo(fstring.format(*numbers, **variables), nl=False)
        except Exception as err:
            format_opt = next(
                a for a in ctx.command.params if a.human_readable_name == "fstring"
            )
            hint = format_opt.get_error_hint(ctx)
            ctx.fail(f"Invalid value for {hint}: {str(err)}")
    # Print final newline
    click.echo("\n", nl=False)
