import pytest

from src.formatter import _status_tag, format_fuzzy_set, format_result, format_table
from src.knowledge_base import KnowledgeBase


class TestFormatFuzzySet:
    def test_empty(self):
        assert format_fuzzy_set({}) == "{}"

    def test_single(self):
        assert format_fuzzy_set({"x": 0.5}) == "{<x, 0.5>}"

    def test_multiple(self):
        out = format_fuzzy_set({"x": 0.5, "y": 1.0})
        assert out == "{<x, 0.5>, <y, 1>}"


class TestFormatTable:
    def test_empty(self):
        out = format_table("T", {})
        assert "=== T ===" in out
        assert "(пустая таблица)" in out

    def test_normal(self):
        table = {"A": {"x": 0.12345, "y": 1.0}, "B": {"x": 0.0, "y": 0.5}}
        out = format_table("T", table)
        assert "=== T ===" in out
        assert "x" in out and "y" in out
        assert "A" in out and "B" in out


class TestStatusTag:
    def test_new(self):
        assert _status_tag("B1'", "new") == "новый -> B1'"

    def test_duplicate(self):
        assert _status_tag("B", "duplicate") == "дубликат B"

    def test_covered(self):
        assert _status_tag("B", "covered") == "поглощён B"

    def test_unknown_status(self):
        with pytest.raises(KeyError):
            _status_tag("B", "unknown")


class TestFormatResult:
    def _write_input(self, tmp_path, content):
        p = tmp_path / "sample.txt"
        p.write_text(content, encoding="utf-8")
        return str(p)

    def test_basic_duplicate(self, tmp_path):
        path = self._write_input(tmp_path, "A={<x,0.5>}\nB={<x,0.5>}\n\nA(x)~>B(y)\n")
        kb = KnowledgeBase({"A": {"x": 0.5}, "B": {"x": 0.5}})
        deriv = ("A(x)~>B(y)", "A", {"x": {"x": 1.0}}, {"x": 0.5}, "B", "duplicate")
        result = {
            "rules_parsed": [("A(x)~>B(y)", "A", "B")],
            "relations": {"A(x)~>B(y)": {"x": {"x": 1.0}}},
            "skipped_rules": [],
            "iterations_log": [(1, [deriv], [], [("B", "duplicate")])],
            "kb": kb,
        }
        out = format_result(result, path)
        assert "Входные данные:" in out
        assert "R = I(A(x)~>B(y))" in out
        assert "Итерация 1" in out
        assert "Выведенный факт:" in out
        assert "дубликат B" in out
        assert "Итоговая база знаний" in out
        assert "A = {<x, 0.5>}" in out
        assert "B = {<x, 0.5>}" in out

    def test_no_derivations(self, tmp_path):
        path = self._write_input(tmp_path, "A={}\n")
        kb = KnowledgeBase({"A": {}})
        result = {
            "rules_parsed": [],
            "relations": {},
            "skipped_rules": [],
            "iterations_log": [(1, [], [], [])],
            "kb": kb,
        }
        out = format_result(result, path)
        assert "(нет применимых правил)" in out
        assert "Итоговая база знаний" in out
        assert "A = {}" in out

    def test_new_fact(self, tmp_path):
        path = self._write_input(tmp_path, "A={<x,0.5>}\nB={<x,0.6>}\n\nA(x)~>B(y)\n")
        kb = KnowledgeBase({"A": {"x": 0.5}, "B": {"x": 0.6}, "B1'": {"x": 1.0}})
        deriv = ("A(x)~>B(y)", "C", {"x": {"x": 1.0}}, {"x": 1.0}, "B1'", "new")
        result = {
            "rules_parsed": [("A(x)~>B(y)", "A", "B")],
            "relations": {"A(x)~>B(y)": {"x": {"x": 1.0}}},
            "skipped_rules": [],
            "iterations_log": [(1, [deriv], ["B1'"], [])],
            "kb": kb,
        }
        out = format_result(result, path)
        assert "Добавлено: B1'" in out
        assert "новый -> B1'" in out
        assert "B1' = {<x, 1>}" in out

    def test_matched_only_no_new(self, tmp_path):
        path = self._write_input(tmp_path, "A={<x,0.5>}\nB={<x,0.6>}\n\nA(x)~>B(y)\n")
        kb = KnowledgeBase({"A": {"x": 0.5}, "B": {"x": 0.6}})
        deriv = ("A(x)~>B(y)", "A", {"x": {"x": 1.0}}, {"x": 0.5}, "B", "covered")
        result = {
            "rules_parsed": [("A(x)~>B(y)", "A", "B")],
            "relations": {"A(x)~>B(y)": {"x": {"x": 1.0}}},
            "skipped_rules": [],
            "iterations_log": [(1, [deriv], [], [("B", "covered")])],
            "kb": kb,
        }
        out = format_result(result, path)
        assert "Все результаты совпали с существующими: B." in out
        assert "сходимость достигнута" in out.lower()

    def test_multiple_iterations(self, tmp_path):
        path = self._write_input(tmp_path, "A={<x,0.5>}\nB={<x,0.6>}\n\nA(x)~>B(y)\n")
        kb = KnowledgeBase({"A": {"x": 0.5}, "B": {"x": 0.6}})
        d1 = ("A(x)~>B(y)", "A", {"x": {"x": 1.0}}, {"x": 0.5}, "B", "covered")
        result = {
            "rules_parsed": [("A(x)~>B(y)", "A", "B")],
            "relations": {"A(x)~>B(y)": {"x": {"x": 1.0}}},
            "skipped_rules": [],
            "iterations_log": [
                (1, [d1], [], [("B", "covered")]),
                (2, [], [], []),
            ],
            "kb": kb,
        }
        out = format_result(result, path)
        assert "Итерация 1" in out
        assert "Итерация 2" in out
        assert "(нет применимых правил)" in out
