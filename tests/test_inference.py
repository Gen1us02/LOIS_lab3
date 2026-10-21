from src.inference import run_inference


def test_run_inference_missing_file():
    assert run_inference("no_such_file_12345.txt") == []


def test_run_inference_load_error(tmp_path):
    p = tmp_path / "bad.txt"
    p.write_text("A={<x,0>}", encoding="utf-8")
    res = run_inference(str(p))
    text = "".join(res)
    assert "Ошибка загрузки данных" in text


def test_run_inference_missing_fact(tmp_path):
    p = tmp_path / "missing_fact.txt"
    p.write_text(
        "A={<x,0.5>}\n" "\n" "A(x)~>B(y)\n",
        encoding="utf-8",
    )
    res = run_inference(str(p))
    text = "".join(res)
    assert "Ошибка: факт 'B' не найден." in text


def test_run_inference_normal(tmp_path):
    p = tmp_path / "ok.txt"
    p.write_text(
        "A={<x,0.5>,<y,1>}\n"
        "B={<x,1>,<y,0.5>}\n"
        "C={<z,0.5>}\n"
        "D={<x,0.5>}\n"
        "\n"
        "A(x)~>B(y)\n",
        encoding="utf-8",
    )
    res = run_inference(str(p))
    text = "".join(res)
    assert "--- Пример: ok.txt ---" in text
    assert "=== Правило: A(x)~>B(y) ===" in text
    assert "Результат:" in text
    assert "I1 =" in text


def test_run_inference_disjoint_symbols(tmp_path):
    """Покрывает ветку `continue`: факт не имеет общих символов с антецедентом."""
    p = tmp_path / "disjoint.txt"
    p.write_text(
        "A={<x,0.5>}\n" "B={<x,1>}\n" "C={<z,0.7>}\n" "\n" "A(x)~>B(y)\n",
        encoding="utf-8",
    )
    res = run_inference(str(p))
    text = "".join(res)
    assert "=== Правило: A(x)~>B(y) ===" in text
    assert "Результат:" in text


def test_run_inference_multiple_rules(tmp_path):
    """Покрывает ветку с несколькими правилами (rule_relations заполняется многократно)."""
    p = tmp_path / "multi.txt"
    p.write_text(
        "A={<x,0.5>}\n"
        "B={<x,1>,<y,0.3>}\n"
        "C={<y,0.8>}\n"
        "\n"
        "A(x)~>B(y)\n"
        "B(y)~>C(x)\n",
        encoding="utf-8",
    )
    res = run_inference(str(p))
    text = "".join(res)
    assert "Правило: A(x)~>B(y)" in text
    assert "Правило: B(y)~>C(x)" in text
