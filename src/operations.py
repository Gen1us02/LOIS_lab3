"""
Лабораторная работа №1 по дисциплине ЛОИС
Выполнили студенты группы 421702 БГУИР:
    - Кулик Е.Д.
    - Поплавский К.Д.
    - Перерва П.Д.
28.09.2026


Файл отвечает за реализацию операций нечёткой логики:
    - импликация Гогена,
    - треугольная норма (произведение),
    - построение отношения и таблицы вывода,
    - сжатие (max по столбцу).

Источники:
Блюмин, С. Л. Нечёткая логика: алгебраические основы и приложения /
С. Л. Блюмин, И. А. Шуйкова, П. В. Сараев, И. В. Черпаков. –
Липецк : ЛЭГИ, 2002. – 111 с.
"""


def gogen_impl(a, b):
    """Импликация Гогена: 1 при a <= b, иначе b/a. При a=0 -> 1."""
    if a == 0:
        return 1.0
    return min(1.0, b / a)


def t_norm(a, b):
    """T-норма — алгебраическое произведение."""
    return a * b


def matrix_impl(set1, set2):
    """Матрица отношения R[x][y] = I(A(x), B(y))."""
    return {x: {y: gogen_impl(set1[x], set2[y]) for y in set2} for x in set1}


def built_impl_table(A_prime, relation):
    """Таблица T(A'(x), R(x,y)). Отсутствующий x -> A'(x)=0."""
    if not relation:
        return {}
    return {
        x: {y: t_norm(A_prime.get(x, 0.0), r_xy) for y, r_xy in relation[x].items()}
        for x in relation
    }


def compress(impl_table):
    """Сжатие: max по столбцу (sup по x)."""
    if not impl_table:
        return {}
    col_keys = list(next(iter(impl_table.values())).keys())
    return {y: max(row[y] for row in impl_table.values()) for y in col_keys}
