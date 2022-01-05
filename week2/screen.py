"""
Peer-graded Assignment: Создание иерархий классов.
Задача: Провести рефакторниг кода, переписать программу в ООП стиле с использованием классов и наследования.

Дополнительный функционал:
 1. Реализована возможность удаления последней «опорной» точки из кривой по правой копке мыши.
 2. Реализована возможность отрисовки на экране нескольких кривых (добавление кривой по A)
"""

import random
import math
import pygame

SCREEN_DIM = (800, 600)


class Vec2d:
    """
    Класс 2-мерных векторов. В классе определены методы для основных математических операций,
    необходимых для работы с векторами
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tup = (x, y)

    def __add__(self, other):
        """возвращает сумму двух векторов"""
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """"возвращает разность двух векторов"""
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, k):
        """возвращает произведение вектора на число"""
        return Vec2d(self.x * k, self.y * k)

    def __len__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __getitem__(self, index):
        return self.tup[index]

    def int_pair(self, x, y):
        """возвращает кортеж из двух целых чисел (текущие координаты вектора)"""
        return self.tup


class Polyline:
    """
    Класс замкнутых ломаных Polyline с методами отвечающими за добавление в ломаную точки (Vec2d) c её скоростью,
    пересчёт координат точек (set_points)
    и отрисовку ломаной (draw_points).
    """
    def __init__(self):
        self.points = []
        self.speeds = []

    def add_point(self, point):
        self.points.append(point)

    def add_speed(self, speed):
        self.speeds.append(speed)

    def del_last_point(self):
        if len(self.points) > 0:
            self.points.pop(-1)

    def del_last_speed(self):
        if len(self.speeds) > 0:
            self.speeds.pop(-1)

    def set_points(self):
        """функция перерасчета координат опорных точек"""
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]

            if self.points[p][0] > SCREEN_DIM[0] or self.points[p][0] < 0:
                self.speeds[p] = Vec2d(-self.speeds[p][0], self.speeds[p][1])
            if self.points[p][1] > SCREEN_DIM[1] or self.points[p][1] < 0:
                self.speeds[p] = Vec2d(self.speeds[p][0], -self.speeds[p][1])

    def draw_points(self, width=3, color=(255, 255, 255)):
        """функция отрисовки точек на экране"""
        for p in self.points:
            pygame.draw.circle(gameDisplay, color,
                               (int(p[0]), int(p[1])), width)

    def clear_all(self):
        self.points = []
        self.speeds = []


class Knot(Polyline):
    """
    Класс Knot (наследник класса Polyline), в котором добавление и пересчёт координат инициируют
    вызов функции get_knot для расчёта точек кривой по добавляемым «опорным» точкам
    """
    def __init__(self):
        super().__init__()
        self._steps = 0

    def set_steps(self, steps):
        self._steps = steps

    def get_steps(self):
        return self._steps

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self, count):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            res.extend(self.get_points(ptn, count))
        return res

    @staticmethod
    def draw_line(points, width, color):
        for p_n in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, color,
                             (int(points[p_n][0]), int(points[p_n][1])),
                             (int(points[p_n + 1][0]), int(points[p_n + 1][1])), width)

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        if style == "points":
            super().draw_points()
        elif style == "line":
            self.draw_line(self.get_knot(self._steps), width, color)


# =======================================================================================
# Функции отрисовки
# =======================================================================================
def draw_help():
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show/Hide Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append(["A", "Add new line"])
    data.append(["Mouse left", "Add anchor point "])
    data.append(["Mouse right", "Delete last anchor point "])
    data.append(["", ""])
    data.append([str(knots[-1].get_steps()), "Current points"])
    data.append([str(len(knots)), "Number of lines "])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (280, 100 + 30 * i))


# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    knots = [Knot()]

    steps = 35
    working = True
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    [k.clear_all() for k in knots]
                    steps = 35
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                if event.key == pygame.K_a:
                    # Press 'A' add new line
                    knots.append(Knot())
                    steps = 35

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Press left mouse button - add point
                    knots[-1].add_point(Vec2d(event.pos[0], event.pos[1]))
                    knots[-1].add_speed(Vec2d(random.random() * 2, random.random() * 2))
                elif event.button == 3:
                    # Press right mouse button - delete last point
                    knots[-1].del_last_point()
                    knots[-1].del_last_speed()

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        for i, knot in enumerate(knots):
            color.hsla = ((hue * i) % 360, 100, 50, 100)

            knot.set_steps(steps)
            knot.draw_points(style="points")
            knot.draw_points(style="line", width=3, color=color)
            if not pause:
                knot.set_points()

        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
