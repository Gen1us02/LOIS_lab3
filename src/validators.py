"""
Лабораторная работа №1 по дисциплине ЛОИС
Выполнили студенты группы 421702 БГУИР:
    - Кулик Е.Д.
    - Поплавский К.Д.
    - Перерва П.Д.
26.09.2026


Файл отвечает за валидацию правил и фактов.

Источники:
Regular expression operations // Python documentation : [сайт].
– URL: https://docs.python.org/3/library/re.html (дата обращения: 26.09.2026).
"""

import re
from src.exceptions import InvalidFactException, InvalidRuleException


class Fact:
    def __init__(self, fact: str, valid_check: bool = True) -> None:
        self.fact = fact

        if valid_check and not self.__is_valid():
            raise InvalidFactException(fact)

        self.head = self.__get_head()
        self.tail = self.__get_tail()

        if not self.__tail_is_valid():
            raise InvalidFactException(fact)

        self.tail = {pair[0]: pair[1] for pair in self.tail}

    def __is_valid(self):
        pattern = re.compile(
            r"^([A-Z]\d*)\s*=\s*\{\s*"
            r"(?:<([a-z]),\s*(0(?:\.\d+)?|1(?:\.0+)?)>\s*"
            r"(?:,\s*<([a-z]),\s*(0(?:\.\d+)?|1(?:\.0+)?)>)*\s*)?"
            r"\}$"
        )
        match = pattern.match(self.fact)
        if not match:
            return False

        elements = re.findall(r"<([a-z]),", self.fact)
        if len(elements) != len(set(elements)):
            return False

        return True

    def __get_head(self):
        head_tail_pattern = r"^(.+)={(.*)}$"
        fact_name = re.match(head_tail_pattern, self.fact).group(1)  # type: ignore
        return fact_name

    def __get_tail(self):
        head_tail_pattern = r"^(.+)={(.*)}$"
        pairs_str = re.match(head_tail_pattern, self.fact).group(2).strip()  # type: ignore
        if not pairs_str:
            return tuple()
        elements = re.findall(r"<([a-z]),\s*([0-1](?:\.\d+)?)>", pairs_str)
        tail = tuple((symbol, float(value)) for symbol, value in elements)
        return tail

    def __tail_is_valid(self):
        symbols = list(map(lambda x: x[0], self.tail))
        return len(set(symbols)) == len(symbols)


class Rule:
    def __init__(self, rule: str) -> None:
        self.rule = rule

        if not self.__is_valid():
            raise InvalidRuleException(rule)

        self.tail = self.__get_tail()

    def __is_valid(self):
        pattern = re.compile(r"^([A-Z]\d*)\(([a-z])\)\s*~>\s*([A-Z]\d*)\(([a-z])\)$")
        m = pattern.match(self.rule)
        return bool(m and m.group(2) != m.group(4))

    def __get_tail(self):
        return tuple(self.rule.split("~>"))
