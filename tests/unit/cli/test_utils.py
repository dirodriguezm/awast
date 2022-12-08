#!/usr/bin/env python3
from awast.cli.utils import value_parser, parse_nested


def test_parse_nested():
    result = {}
    parse_nested(["resources", "requests", "cpu=10m"], result)
    assert result == {"resources": {"requests": {"cpu": "10m"}}}


def test_parse_nested_chained():
    result = {}
    parse_nested(["uno", "dos", "tres=1"], result)
    parse_nested(["uno", "dos", "cuatro=2"], result)
    parse_nested(["uno", "cinco=3"], result)
    assert result == {
        "uno": {"dos": {"tres": "1", "cuatro": "2"}, "cinco": "3"}
    }


def test_parse_nested_chained_repeaeted():
    result = {}
    parse_nested(["uno", "dos", "tres=1"], result)
    parse_nested(["uno", "dos", "tres=2"], result)
    assert result == {"uno": {"dos": {"tres": "2"}}}


def test_value_parser():
    result = value_parser(["version=1"])
    assert result == {"version": "1"}


def test_value_parser_with_nested():
    result = value_parser(
        [
            "version=1",
            "resources.requests.cpu=10m",
            "resources.requests.mem=10M",
        ]
    )
    assert result == {
        "version": "1",
        "resources": {"requests": {"cpu": "10m", "mem": "10M"}},
    }
