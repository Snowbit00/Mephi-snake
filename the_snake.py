"""Игра «Змейка» на Pygame, написанная на принципах ООП.

Змейка ползёт по полю из клеток, ест яблоки и растёт. Сквозь стены
она проходит насквозь, а при столкновении с собой игра начинается заново.
Управление стрелками, выход по закрытию окна.
"""

from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Центр поля, выровненный по сетке:
SCREEN_CENTER = (
    (GRID_WIDTH // 2) * GRID_SIZE,
    (GRID_HEIGHT // 2) * GRID_SIZE,
)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игрового объекта.

    Хранит позицию и цвет, общие для всех объектов на поле,
    и умеет рисовать одну клетку. Конкретную отрисовку
    задают дочерние классы в методе draw.
    """

    def __init__(self, body_color=None):
        """Создать объект в центре поля с заданным цветом."""
        self.position = SCREEN_CENTER
        self.body_color = body_color

    def draw(self):
        """Отрисовать объект на экране.

        Абстрактный метод: переопределяется в дочерних классах.
        """
        pass

    def draw_cell(self, position):
        """Нарисовать одну клетку цветом объекта с рамкой."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Яблоко, которое появляется в случайной свободной клетке."""

    def __init__(self, body_color=APPLE_COLOR, occupied_positions=()):
        """Создать яблоко и сразу поставить его в случайную клетку.

        occupied_positions — клетки, куда яблоко ставить нельзя
        (например, занятые змейкой).
        """
        super().__init__(body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=()):
        """Переставить яблоко в случайную клетку вне occupied_positions."""
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if position not in occupied_positions:
                self.position = position
                return

    def draw(self):
        """Отрисовать яблоко."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Змейка: список координат сегментов, голова — первый элемент."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Создать змейку из одной головы в центре поля."""
        super().__init__(body_color)
        self.reset()

    def reset(self):
        """Вернуть змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Применить направление, выбранное нажатием клавиши."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Вернуть координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Сдвинуть змейку на одну клетку по направлению движения.

        Новая голова добавляется в начало списка. Если змейка не
        выросла, последний сегмент удаляется и запоминается в
        self.last, чтобы затереть его на экране. Выход за край поля
        переносит голову на противоположную сторону.
        """
        head_x, head_y = self.get_head_position()
        step_x, step_y = self.direction
        new_head = (
            (head_x + step_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + step_y * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Затереть след хвоста и отрисовать все сегменты змейки."""
        if self.last is not None:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        for position in self.positions:
            self.draw_cell(position)


def handle_keys(game_object):
    """Обработать события: закрытие окна и нажатия стрелок.

    Разворот на 180 градусов запрещён: змейка не может
    сразу поползти назад.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Запустить игру: создать объекты и выполнять игровой цикл."""
    # Инициализация PyGame:
    pygame.init()
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
