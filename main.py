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

Основной файл программы.

Источники:
Блюмин, С. Л. Нечёткая логика: алгебраические основы и приложения /
С. Л. Блюмин, И. А. Шуйкова, П. В. Сараев, И. В. Черпаков. –
Липецк : ЛЭГИ, 2002. – 111 с.

os — Miscellaneous operating system interfaces : [документация Python].
– URL: https://docs.python.org/3/library/os.html (дата обращения: 28.09.2026).
"""

import os

from src.inference import run_inference


def main(data_dir="data"):
    if not os.path.isdir(data_dir):
        print("Папка с примерами не найдена:", data_dir)
        return
    examples = sorted(os.listdir(data_dir))
    if not examples:
        print("Нет примеров в папке:", data_dir)
        return
    for example in examples:
        file_path = os.path.join(data_dir, example)
        if not os.path.isfile(file_path):
            continue
        print("".join(run_inference(file_path)))
        print("=" * 100 + "\n")


if __name__ == "__main__":
    main("data")
