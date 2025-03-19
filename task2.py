import pygame
import random

# Цвета
blue = (50, 153, 213)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
white = (255, 255, 255)

# Размеры
dis_width = 600
dis_height = 400
snake_block = 10

pygame.init()
display = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Шрифты
font_style = pygame.font.SysFont("Verdana", 20)

# Отрисовка змеи
def print_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(display, black, [x[0], x[1], snake_block, snake_block])

# Отображение счёта и уровня
def show_score(score, level):
    value = font_style.render(f"Score: {score}  Level: {level}", True, white)
    display.blit(value, [10, 10])

# Генерация случайной позиции еды вне змеи
def generate_food(snake_list):
    while True:
        food_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        food_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
        if [food_x, food_y] not in snake_list:
            return food_x, food_y

# Главная функция
def main():
    game_over = False
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    snake_length = 1

    score = 0
    level = 1
    speed = 10

    food_x, food_y = generate_food(snake_list)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        # Проверка выхода за границы
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_over = True

        x1 += x1_change
        y1 += y1_change

        display.fill(blue)
        pygame.draw.rect(display, red, [food_x, food_y, snake_block, snake_block])

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Столкновение с собой
        for block in snake_list[:-1]:
            if block == snake_head:
                game_over = True

        print_snake(snake_block, snake_list)
        show_score(score, level)

        pygame.display.update()

        # Съедание еды
        if x1 == food_x and y1 == food_y:
            food_x, food_y = generate_food(snake_list)
            snake_length += 1
            score += 1

            # Повышение уровня
            if score % 3 == 0:
                level += 1
                speed += 2

        clock.tick(speed)
    pygame.quit()

main()
 