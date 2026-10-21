"""
Лабораторная работа №1 по дисциплине ЛОИС
Выполнили студенты группы 421702 БГУИР:
    - Кулик Е.Д.
    - Поплавский К.Д.
    - Перерва П.Д.
26.09.2026

Файл, содержащий реализацию исключений программы
"""


class InvalidFactException(Exception):
    def __init__(self, fact: str) -> None:
        super().__init__(f"Invalid format of fact: {fact}")


class InvalidRuleException(Exception):
    def __init__(self, rule: str) -> None:
        super().__init__(f"Invalid format of rule: {rule}")
