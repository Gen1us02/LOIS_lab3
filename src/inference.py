"""
Лабораторная работа №1 по дисциплине ЛОИС
Выполнили студенты группы 421702 БГУИР:
    - Кулик Е.Д.
    - Поплавский К.Д.
    - Перерва П.Д.
28.09.2026

Прямой нечёткий логический вывод:
    - читает пример из файла,
    - строит отношения для каждого правила,
    - применяет композицию и сжатие,
    - возвращает список строк отчёта.
"""

import os
from collections import defaultdict

from src import operations
from src.formatter import format_table
from src.loader import load_from_file


def run_inference(file_path):
    solution = []
    if not os.path.isfile(file_path):
        return solution

    solution.append(f"\n--- Пример: {os.path.basename(file_path)} ---\n")
    solution.append("Входные данные:\n")
    with open(file_path, "r", encoding="utf-8") as f:
        solution.append(f.read())
    solution.append("\n\nПрямой нечеткий вывод:\n")

    try:
        facts, rules = load_from_file(file_path)
    except Exception as e:
        solution.append(f"Ошибка загрузки данных: {e}\n")
        return solution

    # ---------- 1. Матрицы отношений ----------
    rule_relations = {}
    for rule_obj in rules.values():
        names = [t.strip().split("(")[0] for t in rule_obj.tail]
        first_name, second_name = names[0], names[1]
        if first_name not in facts or second_name not in facts:
            missing = first_name if first_name not in facts else second_name
            solution.append(f"Ошибка: факт '{missing}' не найден.\n")
            return solution
        rule_relations[rule_obj.rule] = operations.matrix_impl(
            facts[first_name].tail, facts[second_name].tail
        )

    # ---------- 2. Сколько результатов на каждое следствие ----------
    # Ключ — имя следствия (B, C, ...), значение — сколько раз оно встретится
    counts = defaultdict(int)
    for rule_name in rule_relations:
        rule_obj = rules[rule_name]
        names = [t.strip().split("(")[0] for t in rule_obj.tail]
        consequent_name = names[1]
        antecedent_keys = set(facts[names[0]].tail.keys())  # type: ignore
        for _, fact in facts.items():
            if set(fact.tail.keys()) & antecedent_keys:  # type: ignore
                counts[consequent_name] += 1

    # ---------- 3. Печать ----------
    result_lines = []
    indices = defaultdict(int)

    for rule_name, relation in rule_relations.items():
        rule_obj = rules[rule_name]
        names = [t.strip().split("(")[0] for t in rule_obj.tail]
        antecedent_name, consequent_name = names[0], names[1]
        antecedent_keys = set(facts[antecedent_name].tail.keys())  # type: ignore

        solution.append(f"\n=== Правило: {rule_name} ===")
        solution.append(format_table(f"R = I({antecedent_name})", relation))

        for _, fact in facts.items():
            if not (set(fact.tail.keys()) & antecedent_keys):  # type: ignore
                continue

            table = operations.built_impl_table(fact.tail, relation)
            compressed = operations.compress(table)

            # Имя: B' если единственный результат; иначе B1', B2', ...
            if counts[consequent_name] == 1:
                name = f"{consequent_name}'"
            else:
                indices[consequent_name] += 1
                name = f"{consequent_name}{indices[consequent_name]}'"

            source = f"({rule_name})/~\\{fact.head}'"
            solution.append(format_table(f"{source}", table))

            tail_str = (
                "{" + ", ".join(f"<{k}, {v}>" for k, v in compressed.items()) + "}"
            )
            result_lines.append(f"{name} = {tail_str}")

    solution.append("\nРезультат:\n")
    for line in result_lines:
        solution.append(line + "\n")

    return solution
