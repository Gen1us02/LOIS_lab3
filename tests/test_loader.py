import pytest

from src.exceptions import InvalidFactException, InvalidRuleException
from src.loader import get_facts_dict, get_rules_dict, load_from_file
from src.validators import Fact, Rule


def test_load_from_file_valid(tmp_path):
    p = tmp_path / "data.txt"
    p.write_text(
        "A={<x,0>,<y,1>}\n" "B={<x,1>,<y,0>}\n" "\n" "A(x)~>B(y)\n" "B(y)~>A(x)\n",
        encoding="utf-8",
    )
    facts, rules = load_from_file(str(p))
    assert set(facts.keys()) == {"A", "B"}
    assert facts["A"].tail == {"x": 0.0, "y": 1.0}
    assert set(rules.keys()) == {"A(x)~>B(y)", "B(y)~>A(x)"}


def test_load_from_file_less_than_two_blocks(tmp_path):
    p = tmp_path / "bad.txt"
    p.write_text("A={<x,0>}", encoding="utf-8")
    with pytest.raises(ValueError):
        load_from_file(str(p))


def test_load_from_file_extra_blocks_ignored(tmp_path):
    p = tmp_path / "extra.txt"
    p.write_text(
        "A={<x,0>}\n" "\n" "A(x)~>B(y)\n" "\n" "C={<z,0>}\n",
        encoding="utf-8",
    )
    facts, rules = load_from_file(str(p))
    assert set(facts.keys()) == {"A"}
    assert set(rules.keys()) == {"A(x)~>B(y)"}


def test_load_from_file_invalid_fact(tmp_path):
    p = tmp_path / "bad_fact.txt"
    p.write_text("a={<x,0>}\n\nA(x)~>B(y)", encoding="utf-8")
    with pytest.raises(InvalidFactException):
        load_from_file(str(p))


def test_load_from_file_invalid_rule(tmp_path):
    p = tmp_path / "bad_rule.txt"
    p.write_text("A={<x,0>}\n\nA(x)~>A(x)", encoding="utf-8")
    with pytest.raises(InvalidRuleException):
        load_from_file(str(p))


def test_get_facts_dict():
    f1 = Fact("A={<x,0>}")
    f2 = Fact("B={<y,1>}")
    d = get_facts_dict([f1, f2])
    assert d == {"A": f1, "B": f2}


def test_get_rules_dict():
    r1 = Rule("A(x)~>B(y)")
    r2 = Rule("B(y)~>A(x)")
    d = get_rules_dict([r1, r2])
    assert d == {"A(x)~>B(y)": r1, "B(y)~>A(x)": r2}
