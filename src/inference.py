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

from src import operations
from src.formatter import format_table
from src.loader import load_from_file


def run_inference(file_path):
    """Выполняет прямой нечёткий вывод для примера из файла.

    Возвращает список строк отчёта. Если файла нет — пустой список.
    """
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

    # Матрица отношения для каждого правила
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

    # Прямой вывод: для каждого правила перебираем ВСЕ факты как A'
    result_heads, result_sets = [], []

    for rule_name, relation in rule_relations.items():
        rule_obj = rules[rule_name]
        antecedent_name = rule_obj.tail[0].strip().split("(")[0]
        antecedent_keys = set(facts[antecedent_name].tail.keys())  # type: ignore

        solution.append(f"\n=== Правило: {rule_name} ===")
        solution.append(format_table(f"R = I({antecedent_name})", relation))

        for _, fact in facts.items():
            if not (set(fact.tail.keys()) & antecedent_keys):  # type: ignore
                continue

            table = operations.built_impl_table(fact.tail, relation)
            compressed = operations.compress(table)

            head_name = f"({rule_name})/~\\{fact.head}"
            solution.append(format_table(head_name, table))

            result_heads.append(head_name)
            result_sets.append(
                "{" + ", ".join(f"<{k}, {v}>" for k, v in compressed.items()) + "}"
            )

    solution.append("\nРезультат:\n")
    for i, (head, tail) in enumerate(zip(result_heads, result_sets), 1):
        solution.append(f"I{i} = {head} = {tail}\n")

    return solution
