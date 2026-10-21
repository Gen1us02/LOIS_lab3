"""
Лабораторная работа №1 по дисциплине ЛОИС
Выполнили студенты группы 421702 БГУИР:
    - Кулик Е.Д.
    - Поплавский К.Д.
    - Перерва П.Д.
26.09.2026

Модуль загрузки фактов и правил из файла.
"""

from typing import List
from src.validators import Fact, Rule


def load_from_file(path):
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

    blocks = [b for b in content.split("\n\n") if b.strip()]
    if len(blocks) < 2:
        raise ValueError(
            "Файл должен содержать два блока, разделённые пустой строкой: "
            "факты и правила."
        )

    facts_block, rules_block = blocks[0], blocks[1]

    facts_str = [
        "".join(line.split()) for line in facts_block.split("\n") if line.strip()
    ]
    rules_str = [
        "".join(line.split()) for line in rules_block.split("\n") if line.strip()
    ]

    facts = [Fact(fact) for fact in facts_str]
    rules = [Rule(rule) for rule in rules_str]

    return get_facts_dict(facts), get_rules_dict(rules)


def get_facts_dict(facts: List[Fact]):
    return {fact.head: fact for fact in facts}


def get_rules_dict(rules: List[Rule]):
    return {rule.rule: rule for rule in rules}
