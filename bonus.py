import pygame
import random
import ast
import operator
import time

# Настройка окна
pygame.init()
WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Prime Math Challenge")

# Цвета
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
BLUE, RED, GREEN, GRAY = (0, 0, 255), (255, 0, 0), (0, 180, 0), (120, 120, 120)

# Шрифт
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

# Уровни с простыми числами
prime_levels = [
    [2, 3, 5], [7, 11, 13], [17, 19, 23],
    [29, 31, 37], [41, 43, 47], [53, 59, 61],
    [67, 71, 73], [79, 83, 89]
]

# Допустимые арифметические операции
SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg
}

def evaluate(expr):
    try:
        tree = ast.parse(expr, mode="eval")
        return eval_node(tree.body)
    except Exception:
        raise ValueError("Ошибка выражения")

def eval_node(node):
    if isinstance(node, ast.BinOp):
        return SAFE_OPS[type(node.op)](eval_node(node.left), eval_node(node.right))
    elif isinstance(node, ast.UnaryOp):
        return SAFE_OPS[type(node.op)](eval_node(node.operand))
    elif isinstance(node, ast.Num):
        return node.n
    else:
        raise ValueError("Неверное выражение")

class Game:
    def __init__(self):
        self.active = True
        self.stage = 0
        self.number_pool = []
        self.expression = ""
        self.message = ""
        self.success_message = ""
        self.error = ""
        self.awaiting_count = True
        self.count = 0

    def draw_ui(self):
        win.fill(WHITE)

        if self.awaiting_count:
            txt = font.render("Сколько чисел (1-6)? " + self.expression, True, BLUE)
            win.blit(txt, (20, 100))
        else:
            win.blit(font.render(f"Уровень {self.stage + 1}. Найдите: {prime_levels[self.stage]}", True, BLACK), (20, 20))
            win.blit(font.render(f"Числа: {self.number_pool}", True, BLACK), (20, 60))
            win.blit(font.render(f"Выражение: {self.expression}", True, BLUE), (20, 100))
            
            # Подсказка по доступным операциям
            win.blit(small_font.render("Допустимые операции: +  -  *  /  ( )", True, GRAY), (20, 140))

            # Сообщения
            if self.error:
                win.blit(font.render(self.error, True, RED), (20, 180))
            if self.success_message:
                win.blit(font.render(self.success_message, True, GREEN), (20, 220))
            if self.message:
                msg_color = GREEN if "УСПЕШНО" in self.message else RED
                win.blit(font.render(self.message, True, msg_color), (20, 260))

        pygame.display.flip()

    def handle_input(self, char):
        if char.isdigit() or char in "+-*/()":
            self.expression += char

    def generate_numbers(self):
        self.number_pool = [random.randint(1, 6) for _ in range(self.count)]

    def validate_expression(self):
        try:
            result = evaluate(self.expression)
        except ValueError:
            self.error = "Ошибка: выражение неверно"
            self.message = "Неправильно"
            return False

        # Использованные числа
        digits = [int(ch) for ch in self.expression if ch.isdigit()]
        if sorted(digits) != sorted(self.number_pool):
            self.error = "Используйте все выпавшие числа!"
            self.message = "Неправильно"
            return False

        if result in prime_levels[self.stage]:
            self.message = "УСПЕШНО! Вы использовали все числа и получили правильный результат!"
            self.success_message = f"{self.expression} = {int(result)}"
            self.error = ""
            return True
        else:
            self.error = "Результат не соответствует целевым числам!"
            self.message = "Неправильно"
            return False

    def advance_level(self):
        self.stage += 1
        if self.stage >= len(prime_levels):
            self.active = False
        else:
            self.awaiting_count = True
            self.expression = ""
            self.message = ""
            self.success_message = ""
            self.error = ""

    def run(self):
        while self.active:
            self.draw_ui()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.awaiting_count:
                            try:
                                self.count = int(self.expression)
                                if 1 <= self.count <= 6:
                                    self.generate_numbers()
                                    self.awaiting_count = False
                                    self.expression = ""
                                    self.error = ""
                                else:
                                    self.error = "Введите число от 1 до 6"
                                    self.expression = ""
                            except ValueError:
                                self.error = "Введите корректное число"
                                self.expression = ""
                        else:
                            if self.validate_expression():
                                self.draw_ui()
                                pygame.time.delay(1500)  # Показываем успех 1.5 секунды
                                self.advance_level()
                    elif event.key == pygame.K_BACKSPACE:
                        self.expression = self.expression[:-1]
                    else:
                        self.handle_input(event.unicode)
        pygame.quit()

# Запуск игры
if __name__ == "__main__":
    Game().run()
