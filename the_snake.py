"""Игра «Змейка» на Pygame, написанная на принципах ООП.

Змейка ползёт по полю из клеток, ест яблоки и растёт. Сквозь стены
она проходит насквозь, а при столкновении с собой игра начинается заново.
Управление стрелками, выход по закрытию окна.
"""

from random import randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

SCREEN_CENTER = (
    (GRID_WIDTH // 2) * GRID_SIZE,
    (GRID_HEIGHT // 2) * GRID_SIZE,
)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

TURNS = {
    pygame.K_UP: (UP, DOWN),
    pygame.K_DOWN: (DOWN, UP),
    pygame.K_LEFT: (LEFT, RIGHT),
    pygame.K_RIGHT: (RIGHT, LEFT),
}

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игрового объекта.

    Хранит позицию и цвет, общие для всех объектов на поле,
    и умеет рисовать одну клетку. Конкретную отрисовку
    задают дочерние классы в методе draw.
    """

    def __init__(self, position=SCREEN_CENTER, body_color=None):
        """Создать объект в центре поля с заданным цветом."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовать объект на экране.
        Абстрактный метод: переопределяется в дочерних классах.
        """
        raise NotImplementedError(
            f'Метод draw не переопределён в классе {type(self).__name__}')

    def draw_cell(self, position):
        """Нарисовать одну клетку цветом объекта с рамкой."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Яблоко, которое появляется в случайной свободной клетке."""

    def __init__(self, position=SCREEN_CENTER, body_color=APPLE_COLOR,
                 occupied_positions=()):
        """Создать яблоко и сразу поставить его в случайную клетку.
        occupied_positions-клетки, куда яблоко ставить нельзя
        (например, занятые змейкой).
        """
        super().__init__(position, body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=()):
        """Переставить яблоко в случайную клетку вне occupied_positions."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if self.position not in occupied_positions:
                return

    def draw(self):
        """Отрисовать яблоко."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Змейка: список координат сегментов, голова — первый элемент."""

    def __init__(self, position=SCREEN_CENTER, body_color=SNAKE_COLOR):
        """Создать змейку из одной головы в центре поля."""
        super().__init__(position, body_color)
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
        """Затереть след хвоста и отрисовать новую голову змейки."""
        if self.last is not None:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        self.draw_cell(self.get_head_position())


def handle_keys(game_object):
    """Обработать события: закрытие окна, Esc и нажатия стрелок.
    
    Разворот на 180 градусов запрещён:
    змейка не может сразу поползти назад.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            elif event.key in TURNS:
                new_direction, opposite = TURNS[event.key]
                if game_object.direction != opposite:
                    game_object.next_direction = new_direction


def main():
    """Запустить игру: создать объекты и выполнять игровой цикл."""
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
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
