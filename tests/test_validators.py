import pytest

from src.exceptions import InvalidFactException, InvalidRuleException
from src.validators import Fact, Rule


class TestFact:
    def test_valid_simple(self):
        f = Fact("A={<x,0>}")
        assert f.fact == "A={<x,0>}"
        assert f.head == "A"
        assert f.tail == {"x": 0.0}

    def test_valid_multiple_and_spaces(self):
        # Пробелы допускаются внутри хвоста; перед '=' пробел не допускается
        # (паттерн __get_head: r"^(.+)={(.*)}$").
        f = Fact("A1={<x, 0.5>, <y, 1>}")
        assert f.head == "A1"
        assert f.tail == {"x": 0.5, "y": 1.0}

    def test_invalid_space_before_equals(self):
        # Документируем известное ограничение парсера:
        # пробел перед '=' ломает __get_head (AttributeError).
        with pytest.raises(AttributeError):
            Fact("A1 = {<x, 0.5>}")

    def test_valid_empty_tail(self):
        f = Fact("A={}")
        assert f.head == "A"
        assert f.tail == {}

    def test_invalid_duplicate_symbols(self):
        with pytest.raises(InvalidFactException):
            Fact("A={<x,0>,<x,1>}")

    def test_invalid_name(self):
        with pytest.raises(InvalidFactException):
            Fact("a={<x,0>}")

    def test_invalid_value(self):
        with pytest.raises(InvalidFactException):
            Fact("A={<x,1.5>}")

    def test_invalid_format(self):
        with pytest.raises(InvalidFactException):
            Fact("A={x,0}")

    def test_valid_check_false_bypasses_format(self):
        # 1.5 не проходит __is_valid, но парсится __get_tail
        f = Fact("A={<x,1.5>}", valid_check=False)
        assert f.head == "A"
        assert f.tail == {"x": 1.5}

    def test_tail_duplicate_with_valid_check_false(self):
        with pytest.raises(InvalidFactException):
            Fact("A={<x,0>,<x,1>}", valid_check=False)


class TestRule:
    def test_valid(self):
        r = Rule("A(x)~>B(y)")
        assert r.rule == "A(x)~>B(y)"
        assert r.tail == ("A(x)", "B(y)")

    def test_valid_with_spaces(self):
        r = Rule("A1(x) ~> B2(y)")
        assert r.tail == ("A1(x) ", " B2(y)")

    def test_invalid_same_symbol(self):
        with pytest.raises(InvalidRuleException):
            Rule("A(x)~>B(x)")

    def test_invalid_lowercase_head(self):
        with pytest.raises(InvalidRuleException):
            Rule("a(x)~>B(y)")

    def test_invalid_format(self):
        with pytest.raises(InvalidRuleException):
            Rule("A(x) -> B(y)")
