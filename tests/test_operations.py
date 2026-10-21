import pytest

from src import operations


def test_gogen_impl():
    assert operations.gogen_impl(0, 0.5) == 1.0
    assert operations.gogen_impl(0.5, 0.5) == 1.0
    assert operations.gogen_impl(0.8, 0.4) == pytest.approx(0.5)
    assert operations.gogen_impl(0.4, 0.8) == 1.0
    assert operations.gogen_impl(1.0, 0.0) == 0.0


def test_t_norm():
    assert operations.t_norm(0.5, 0.2) == pytest.approx(0.1)


def test_matrix_impl():
    set1 = {"x": 0.8, "y": 0.4}
    set2 = {"a": 0.2, "b": 0.8}
    result = operations.matrix_impl(set1, set2)
    # gogen_impl(0.8, 0.2) = 0.2/0.8 = 0.25
    assert result["x"]["a"] == pytest.approx(0.25)
    # gogen_impl(0.8, 0.8) = 1.0 (a <= b)
    assert result["x"]["b"] == 1.0
    # gogen_impl(0.4, 0.2) = 0.2/0.4 = 0.5
    assert result["y"]["a"] == pytest.approx(0.5)
    # gogen_impl(0.4, 0.8) = 1.0 (a <= b)
    assert result["y"]["b"] == 1.0


def test_built_impl_table():
    relation = {"x": {"a": 0.5, "b": 0.8}, "y": {"a": 0.2, "b": 0.4}}
    a_prime = {"x": 0.5}
    result = operations.built_impl_table(a_prime, relation)
    assert result["x"]["a"] == pytest.approx(0.25)
    assert result["x"]["b"] == pytest.approx(0.4)
    assert result["y"]["a"] == 0.0
    assert result["y"]["b"] == 0.0


def test_built_impl_table_empty_relation():
    assert operations.built_impl_table({"x": 0.5}, {}) == {}


def test_compress():
    table = {"x": {"a": 0.1, "b": 0.5}, "y": {"a": 0.7, "b": 0.2}}
    assert operations.compress(table) == {"a": 0.7, "b": 0.5}


def test_compress_empty():
    assert operations.compress({}) == {}
