from src.formatter import format_table


def test_format_table_empty():
    out = format_table("T", {})
    assert "(пустая таблица)" in out
    assert "=== T ===" in out


def test_format_table_empty_first_row():
    out = format_table("T", {"A": {}})
    assert "(пустая таблица)" in out


def test_format_table_normal():
    table = {"A": {"x": 0.12345, "y": 1.0}, "B": {"x": 0.0, "y": 0.5}}
    out = format_table("T", table)
    assert "=== T ===" in out
    assert "x" in out and "y" in out
    assert "A" in out and "B" in out
    assert "0.1234" in out or "0.1235" in out
