from src.exceptions import InvalidFactException, InvalidRuleException


def test_invalid_fact_exception_message():
    exc = InvalidFactException("A={}")
    assert str(exc) == "Invalid format of fact: A={}"


def test_invalid_rule_exception_message():
    exc = InvalidRuleException("A(x)~>A(x)")
    assert str(exc) == "Invalid format of rule: A(x)~>A(x)"
