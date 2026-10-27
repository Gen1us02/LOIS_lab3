import pytest
from src.knowledge_base import KnowledgeBase


class TestInit:
    def test_copies_tails(self):
        src = {"A": {"x": 0.5}}
        kb = KnowledgeBase(src)
        kb.facts["A"]["x"] = 0.9
        assert src["A"]["x"] == 0.5

    def test_empty(self):
        kb = KnowledgeBase({})
        assert kb.facts == {}


class TestAdd:
    def test_new_when_base_absent(self):
        kb = KnowledgeBase({})
        name, status = kb.add("B", {"x": 0.3})
        assert name == "B'"
        assert status == "new"
        assert kb["B'"] == {"x": 0.3}

    def test_duplicate(self):
        kb = KnowledgeBase({"A": {"x": 0.5}})
        name, status = kb.add("A", {"x": 0.5})
        assert name == "A"
        assert status == "duplicate"

    def test_covered(self):
        kb = KnowledgeBase({"A": {"x": 0.5}})
        name, status = kb.add("A", {"x": 0.3})
        assert name == "A"
        assert status == "covered"

    def test_new_when_not_covered(self):
        kb = KnowledgeBase({"A": {"x": 0.5}})
        name, status = kb.add("A", {"x": 0.8})
        assert name == "A1'"
        assert status == "new"

    def test_second_new_uses_counter(self):
        kb = KnowledgeBase({"A": {"x": 0.5}})
        kb.add("A", {"x": 0.8})
        name, status = kb.add("A", {"x": 0.9})
        assert name == "A2'"
        assert status == "new"

    def test_covered_extra_zero_key(self):
        kb = KnowledgeBase({"A": {"x": 0.5}})
        name, status = kb.add("A", {"x": 0.3, "y": 0.0})
        assert status == "covered"
        assert name == "A"

    def test_not_covered_extra_positive_key(self):
        kb = KnowledgeBase({"A": {"x": 0.5}})
        name, status = kb.add("A", {"x": 0.3, "y": 0.4})
        assert status == "new"


class TestBaseName:
    def test_simple(self):
        kb = KnowledgeBase({})
        assert kb._base_name("A") == "A"

    def test_strip_quotes(self):
        kb = KnowledgeBase({})
        assert kb._base_name("A'") == "A"

    def test_underscore_digit_suffix(self):
        kb = KnowledgeBase({})
        assert kb._base_name("A_1'") == "A"
        assert kb._base_name("A_42") == "A"

    def test_digit_without_underscore_kept(self):
        kb = KnowledgeBase({})
        assert kb._base_name("A1") == "A1"
        assert kb._base_name("A1'") == "A1"


class TestCovers:
    def test_equal(self):
        kb = KnowledgeBase({})
        assert kb._covers({"x": 0.5}, {"x": 0.5})

    def test_larger_covers_smaller(self):
        kb = KnowledgeBase({})
        assert kb._covers({"x": 0.8}, {"x": 0.5})

    def test_smaller_does_not_cover(self):
        kb = KnowledgeBase({})
        assert not kb._covers({"x": 0.3}, {"x": 0.5})

    def test_missing_key_as_zero(self):
        kb = KnowledgeBase({})
        assert kb._covers({"x": 0.5}, {"x": 0.3, "y": 0.0})

    def test_missing_key_positive_not_covered(self):
        kb = KnowledgeBase({})
        assert not kb._covers({"x": 0.5}, {"x": 0.3, "y": 0.2})


class TestUniqueName:
    def test_first_when_base_absent(self):
        kb = KnowledgeBase({})
        assert kb._unique_name("A") == "A'"

    def test_counter_when_base_present(self):
        kb = KnowledgeBase({"A": {"x": 0.5}})
        assert kb._unique_name("A") == "A1'"
        assert kb._unique_name("A") == "A2'"

    def test_counter_skips_existing(self):
        kb = KnowledgeBase({"A": {"x": 0.5}, "A1'": {"x": 0.5}})
        assert kb._unique_name("A") == "A2'"


class TestAccessors:
    def test_getitem(self):
        kb = KnowledgeBase({"A": {"x": 0.5}})
        assert kb["A"] == {"x": 0.5}

    def test_getitem_missing(self):
        kb = KnowledgeBase({})
        with pytest.raises(KeyError):
            _ = kb["X"]

    def test_items(self):
        kb = KnowledgeBase({"A": {"x": 0.5}})
        assert ("A", {"x": 0.5}) in list(kb.items())
