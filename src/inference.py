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
Источники:
Блюмин, С. Л. Нечёткая логика: алгебраические основы и приложения /
С. Л. Блюмин, И. А. Шуйкова, П. В. Сараев, И. В. Черпаков. –
Липецк : ЛЭГИ, 2002. – 111 с.

os — Miscellaneous operating system interfaces : [документация Python].
– URL: https://docs.python.org/3/library/os.html (дата обращения: 28.09.2026).
"""

import os
from src import operations
from src.loader import load_from_file
from src.knowledge_base import KnowledgeBase


def run_inference(file_path, max_iterations=100):
    if not os.path.isfile(file_path):
        return None

    facts, rules = load_from_file(file_path)
    kb = KnowledgeBase({name: fact.tail for name, fact in facts.items()})

    rules_parsed = []
    relations = {}
    skipped_rules = []

    for rule_obj in rules.values():
        names = [t.strip().split("(")[0] for t in rule_obj.tail]
        rule_str, ant, cons = rule_obj.rule, names[0], names[1]

        if not facts[ant].tail:
            skipped_rules.append((rule_str, "пустая посылка"))
            continue
        if not facts[cons].tail:
            skipped_rules.append((rule_str, "пустое следствие"))
            continue

        rules_parsed.append((rule_str, ant, cons))
        relations[rule_str] = operations.matrix_impl(facts[ant].tail, facts[cons].tail)

    iterations_log = []
    applied = set()
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        snapshot = list(kb.items())
        derivations = []
        new_facts = []
        matched_facts = []

        for rule_str, ant, cons in rules_parsed:
            relation = relations[rule_str]
            ant_keys = set(kb[ant].keys())

            for src_name, src_tail in snapshot:
                if (rule_str, src_name) in applied:
                    continue
                applied.add((rule_str, src_name))

                if not (set(src_tail.keys()) & ant_keys):
                    continue

                table = operations.built_impl_table(src_tail, relation)
                compressed = operations.compress(table)
                if not compressed:
                    continue

                name, status = kb.add(cons, compressed)
                derivations.append(
                    (rule_str, src_name, table, compressed, name, status)
                )
                if status == "new":
                    new_facts.append(name)
                else:
                    matched_facts.append((name, status))

        iterations_log.append((iteration, derivations, new_facts, matched_facts))
        if not new_facts:
            break

    return {
        "rules_parsed": rules_parsed,
        "relations": relations,
        "skipped_rules": skipped_rules,
        "iterations_log": iterations_log,
        "kb": kb,
    }
