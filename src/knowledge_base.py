"""
Лабораторная работа №1 по дисциплине ЛОИС
Выполнили студенты группы 421702 БГУИР:
    - Кулик Е.Д.
    - Поплавский К.Д.
    - Перерва П.Д.
28.09.2026

Вариант 2
Реализовать прямой нечёткий логический вывод,
используя треугольную норму {xi} * {yi} и нечёткую импликацию Гогена.

База знаний: уникальность по содержимому, поглощение доминирующими фактами.

Источники:
Блюмин, С. Л. Нечёткая логика: алгебраические основы и приложения /
С. Л. Блюмин, И. А. Шуйкова, П. В. Сараев, И. В. Черпаков. –
Липецк : ЛЭГИ, 2002. – 111 с.
"""

EPS = 1e-9


class KnowledgeBase:
    def __init__(self, initial_facts):
        self.facts = {name: dict(tail) for name, tail in initial_facts.items()}
        self.counters = {}

    def add(self, base_name, tail):
        tail = dict(tail)

        for name, t in self.facts.items():
            if self._base_name(name) != base_name:
                continue

            if t.keys() == tail.keys() and all(abs(t[k] - tail[k]) < EPS for k in tail):
                return name, "duplicate"

        for name, t in self.facts.items():
            if self._base_name(name) == base_name and self._covers(t, tail):
                return name, "covered"

        name = self._unique_name(base_name)
        self.facts[name] = tail
        return name, "new"

    def _base_name(self, name):
        base = name.rstrip("'")
        head, tail = base[0], base[1:]
        if tail.isdigit():
            return head
        return base

    def _covers(self, t, other):
        return all(other[k] <= t.get(k, 0.0) + EPS for k in other)

    def _unique_name(self, base):
        if base not in self.facts:
            return f"{base}'"
        n = self.counters.get(base, 0)
        while True:
            n += 1
            cand = f"{base}{n}'"
            if cand not in self.facts:
                self.counters[base] = n
                return cand

    def __getitem__(self, name):
        return self.facts[name]

    def items(self):
        return self.facts.items()
