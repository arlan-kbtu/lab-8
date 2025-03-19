import pygame
import sys

pygame.init()

# Размеры окна и базовые настройки
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint App")

# Цвета
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Изначальные настройки
clock = pygame.time.Clock()
screen.fill(WHITE)

# Текущие настройки инструмента
drawing = False
start_pos = None
mode = "draw"  # "draw", "rect", "circle", "erase"
color = BLACK
radius = 5

# Кнопки интерфейса
font = pygame.font.SysFont(None, 24)

buttons = {
    "pen": pygame.Rect(10, 10, 60, 30),
    "rect": pygame.Rect(80, 10, 60, 30),
    "circle": pygame.Rect(150, 10, 60, 30),
    "eraser": pygame.Rect(220, 10, 60, 30),
    "black": pygame.Rect(300, 10, 40, 30),
    "red": pygame.Rect(350, 10, 40, 30),
    "green": pygame.Rect(400, 10, 40, 30),
    "blue": pygame.Rect(450, 10, 40, 30),
}


def draw_interface():
    # Рисуем кнопки
    pygame.draw.rect(screen, GRAY, buttons["pen"])
    screen.blit(font.render("Pen", True, BLACK), (buttons["pen"].x + 10, 15))

    pygame.draw.rect(screen, GRAY, buttons["rect"])
    screen.blit(font.render("Rect", True, BLACK), (buttons["rect"].x + 5, 15))

    pygame.draw.rect(screen, GRAY, buttons["circle"])
    screen.blit(font.render("Circle", True, BLACK), (buttons["circle"].x + 3, 15))

    pygame.draw.rect(screen, GRAY, buttons["eraser"])
    screen.blit(font.render("Eraser", True, BLACK), (buttons["eraser"].x + 5, 15))

    pygame.draw.rect(screen, BLACK, buttons["black"])
    pygame.draw.rect(screen, RED, buttons["red"])
    pygame.draw.rect(screen, GREEN, buttons["green"])
    pygame.draw.rect(screen, BLUE, buttons["blue"])


def handle_buttons(pos):
    global mode, color

    if buttons["pen"].collidepoint(pos):
        mode = "draw"
    elif buttons["rect"].collidepoint(pos):
        mode = "rect"
    elif buttons["circle"].collidepoint(pos):
        mode = "circle"
    elif buttons["eraser"].collidepoint(pos):
        mode = "erase"
    elif buttons["black"].collidepoint(pos):
        color = BLACK
    elif buttons["red"].collidepoint(pos):
        color = RED
    elif buttons["green"].collidepoint(pos):
        color = GREEN
    elif buttons["blue"].collidepoint(pos):
        color = BLUE


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if any(button.collidepoint(event.pos) for button in buttons.values()):
                    handle_buttons(event.pos)
                else:
                    drawing = True
                    start_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                end_pos = event.pos
                if mode == "rect":
                    x, y = start_pos
                    w = end_pos[0] - x
                    h = end_pos[1] - y
                    pygame.draw.rect(screen, color, (x, y, w, h), 2)
                elif mode == "circle":
                    center = start_pos
                    radius = int(((end_pos[0] - center[0]) ** 2 + (end_pos[1] - center[1]) ** 2) ** 0.5)
                    pygame.draw.circle(screen, color, center, radius, 2)
                drawing = False

        elif event.type == pygame.MOUSEMOTION:
            if drawing and mode == "draw":
                pygame.draw.line(screen, color, start_pos, event.pos, radius)
                start_pos = event.pos
            elif drawing and mode == "erase":
                pygame.draw.circle(screen, WHITE, event.pos, radius)

    draw_interface()
    pygame.display.update()
    clock.tick(60)
