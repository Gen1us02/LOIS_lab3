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


def format_table(title, table):
    """Возвращает текстовое представление таблицы с заголовком."""
    output = [f"\n=== {title} ==="]
    if not table:
        output.append("(пустая таблица)")
        return "\n".join(output)
    first_row = next(iter(table.values()))
    if not first_row:
        output.append("(пустая таблица)")
        return "\n".join(output)
    headers = list(first_row.keys())
    output.append(" \t" + "\t".join(headers))
    for row_name, row in table.items():
        values = "\t".join(f"{v:.4g}" for v in row.values())
        output.append(f"{row_name}\t{values}")
    return "\n".join(output)
