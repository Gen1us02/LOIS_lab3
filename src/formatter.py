"""
Лабораторная работа №1 по дисциплине ЛОИС
Выполнили студенты группы 421702 БГУИР:
    - Кулик Е.Д.
    - Поплавский К.Д.
    - Перерва П.Д.
28.09.2026

Форматирование таблиц для текстового отчёта.

Источники:
Блюмин, С. Л. Нечёткая логика: алгебраические основы и приложения /
С. Л. Блюмин, И. А. Шуйкова, П. В. Сараев, И. В. Черпаков. –
Липецк : ЛЭГИ, 2002. – 111 с.
"""


def format_fuzzy_set(tail):
    if not tail:
        return "∅"
    return "{" + ", ".join(f"<{k}, {v:.4g}>" for k, v in tail.items()) + "}"


def format_table(title, table):
    """Табличка {row: {col: value}} с табуляцией, как в исходной версии."""
    output = [f"\n=== {title} ==="]
    if not table:
        output.append("(пустая таблица)")
        return "\n".join(output)
    headers = list(next(iter(table.values())).keys())
    output.append(" \t" + "\t".join(headers))
    for row_name, row in table.items():
        values = "\t".join(f"{v:.4g}" for v in row.values())
        output.append(f"{row_name}\t{values}")
    return "\n".join(output)


def _status_tag(name, status):
    return {
        "new": f"новый → {name}",
        "duplicate": f"дубликат {name}",
        "covered": f"поглощён {name}",
    }[status]


def format_result(result, file_path):
    with open(file_path, encoding="utf-8") as f:
        input_text = f.read()

    lines = ["Входные данные:", input_text]

    # Отношения правил
    for rule_str, _, _ in result["rules_parsed"]:
        lines.append(format_table(f"R = I({rule_str})", result["relations"][rule_str]))

    # Итерации прямого нечеткого вывода
    lines.append("\n\n=== Прямой нечёткий вывод ===")
    for iteration, derivations, new_facts, matched_facts in result["iterations_log"]:
        lines.append(f"\n--- Итерация {iteration} ---")
        if not derivations:
            lines.append("(нет применимых правил)")
            continue

        for rule_str, src_name, table, compressed, name, status in derivations:
            lines.append(format_table(f"T({src_name}, R[{rule_str}])", table))
            cons_name = rule_str.split("~>")[1].split("(")[0]
            lines.append(
                f"\nВыведенный факт: {cons_name}' = {format_fuzzy_set(compressed)}"
                f"  [{_status_tag(name, status)}]"
            )

        if new_facts:
            lines.append(f"\nДобавлено: {', '.join(new_facts)}")
        else:
            if matched_facts:
                names = ", ".join(n for n, _ in matched_facts)
                lines.append(f"\nВсе результаты совпали с существующими: {names}.")
            lines.append("Новых фактов нет — сходимость достигнута.")

    # Итоговая база знаний
    lines.append("\n\n=== Итоговая база знаний ===")
    for name, tail in result["kb"].items():
        lines.append(f"{name} = {format_fuzzy_set(tail)}")

    return "\n".join(lines)
