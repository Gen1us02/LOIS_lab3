import pytest

from src.inference import run_inference


def test_missing_file_returns_none():
    assert run_inference("no_such_file_12345.txt") is None


def test_skip_empty_antecedent(tmp_path):
    p = tmp_path / "x.txt"
    p.write_text(
        "A={}\n" "B={<x,0.5>}\n" "\n" "A(x)~>B(y)\n",
        encoding="utf-8",
    )
    result = run_inference(str(p))
    assert result is not None
    assert result["rules_parsed"] == []
    assert len(result["skipped_rules"]) == 1
    _, reason = result["skipped_rules"][0]
    assert reason == "пустая посылка"


def test_skip_empty_consequent(tmp_path):
    p = tmp_path / "x.txt"
    p.write_text(
        "A={<x,0.5>}\n" "B={}\n" "\n" "A(x)~>B(y)\n",
        encoding="utf-8",
    )
    result = run_inference(str(p))
    assert result is not None
    assert result["rules_parsed"] == []
    assert len(result["skipped_rules"]) == 1
    _, reason = result["skipped_rules"][0]
    assert reason == "пустое следствие"


def test_relations_built(tmp_path):
    p = tmp_path / "x.txt"
    p.write_text(
        "A={<x,0.5>}\n" "B={<x,0.6>}\n" "\n" "A(x)~>B(y)\n",
        encoding="utf-8",
    )
    result = run_inference(str(p))
    assert result is not None
    rel = result["relations"]["A(x)~>B(y)"]
    assert rel["x"]["x"] == pytest.approx(1.0)


def test_convergence_after_first_iteration(tmp_path):
    p = tmp_path / "x.txt"
    p.write_text(
        "A={<x,0.8>}\n" "B={<x,0.4>}\n" "\n" "A(x)~>B(y)\n",
        encoding="utf-8",
    )
    result = run_inference(str(p))
    assert result is not None
    assert len(result["iterations_log"]) == 1

    iter1 = result["iterations_log"][0]
    statuses = [d[5] for d in iter1[1]]
    assert "covered" in statuses
    assert "duplicate" in statuses
    assert iter1[2] == []
    assert iter1[3]


def test_new_fact_derived_and_converges_in_two_iterations(tmp_path):
    """
    A={x:0.5}, B={x:0.2}, C={x:0.9}.
    rel = gogen(0.5, 0.2) = 0.4.
      из A: {x:0.5*0.4=0.2}   -> duplicate (совпал с B)
      из B: {x:0.2*0.4=0.08}  -> covered   (B покрывает)
      из C: {x:0.9*0.4=0.36}  -> new, имя "B1'" (B уже занято -> счётчик с 1)
    Iter 2: B1'={x:0.36} -> {x:0.144} -> covered -> сходимость.
    """
    p = tmp_path / "x.txt"
    p.write_text(
        "A={<x,0.5>}\n" "B={<x,0.2>}\n" "C={<x,0.9>}\n" "\n" "A(x)~>B(y)\n",
        encoding="utf-8",
    )
    result = run_inference(str(p))
    assert result is not None

    assert "B1'" in result["kb"].facts
    assert result["kb"]["B1'"] == {"x": pytest.approx(0.36)}

    assert len(result["iterations_log"]) == 2
    assert result["iterations_log"][0][2] == ["B1'"]
    assert result["iterations_log"][1][2] == []


def test_no_symbol_intersection_is_skipped(tmp_path):
    """Факт без общих символов с антецедентом пропускается (continue)."""
    p = tmp_path / "x.txt"
    p.write_text(
        "A={<x,0.5>}\n" "D={<z,0.3>}\n" "B={<x,0.6>}\n" "\n" "A(x)~>B(y)\n",
        encoding="utf-8",
    )
    result = run_inference(str(p))
    assert result is not None
    iter1 = result["iterations_log"][0]
    src_names = [d[1] for d in iter1[1]]
    assert "D" not in src_names


def test_max_iterations_limits_expansion(tmp_path):
    """max_iterations=1 обрывает вывод даже при появлении нового факта."""
    p = tmp_path / "x.txt"
    p.write_text(
        "A={<x,0.5>}\n" "B={<x,0.2>}\n" "C={<x,0.9>}\n" "\n" "A(x)~>B(y)\n",
        encoding="utf-8",
    )
    result = run_inference(str(p), max_iterations=1)
    assert result is not None
    assert len(result["iterations_log"]) == 1
    assert "B1'" in result["iterations_log"][0][2]


def test_kb_initial_facts_present(tmp_path):
    p = tmp_path / "x.txt"
    p.write_text(
        "A={<x,0.5>}\n" "B={<x,0.6>}\n" "\n" "A(x)~>B(y)\n",
        encoding="utf-8",
    )
    result = run_inference(str(p))
    assert result is not None
    assert "A" in result["kb"].facts
    assert "B" in result["kb"].facts


def test_rules_parsed_structure(tmp_path):
    p = tmp_path / "x.txt"
    p.write_text(
        "A={<x,0.5>}\n" "B={<x,0.6>}\n" "\n" "A(x)~>B(y)\n",
        encoding="utf-8",
    )
    result = run_inference(str(p))
    assert result is not None
    assert len(result["rules_parsed"]) == 1
    rule_str, ant, cons = result["rules_parsed"][0]
    assert rule_str == "A(x)~>B(y)"
    assert ant == "A"
    assert cons == "B"


def test_applied_prevents_reprocessing(tmp_path):
    """
    Во 2-й итерации исходные A, B, C уже в `applied` — они не должны
    обрабатываться повторно. Обрабатывается только новый B1'.
    """
    p = tmp_path / "x.txt"
    p.write_text(
        "A={<x,0.5>}\n" "B={<x,0.2>}\n" "C={<x,0.9>}\n" "\n" "A(x)~>B(y)\n",
        encoding="utf-8",
    )
    result = run_inference(str(p))
    assert result is not None
    assert len(result["iterations_log"]) == 2

    iter2 = result["iterations_log"][1]
    iter2_srcs = [d[1] for d in iter2[1]]
    assert iter2_srcs == ["B1'"]
