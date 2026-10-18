# Изгиб Питона

Учебный проект: игра «Змейка» на Python и Pygame. Написана на ООП: базовый класс `GameObject` и два наследника, `Apple` и `Snake`.

## Как играть

Змейка управляется стрелками. Нужно собирать яблоки: от каждого змейка становится длиннее на одну клетку. Через стены можно проходить насквозь. Если врезаться в себя, игра начинается заново.

## Как запустить

Нужен Python 3.12.

```bash
py -3.12 -m venv venv
.\venv\Scripts\python -m pip install -r requirements.txt
.\venv\Scripts\python the_snake.py
```

На Linux и macOS вместо `.\venv\Scripts\python` пишите `venv/bin/python`.

## Тесты и стиль кода

```bash
.\venv\Scripts\python -m pytest
.\venv\Scripts\python -m flake8
```
