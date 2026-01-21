import pygame
import random
import os

pygame.mixer.init()
pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Background Images
bgimg = pygame.image.load("snake-game-bg.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

welbgimg = pygame.image.load("Snake-welcome.jpg")
welbgimg = pygame.transform.scale(welbgimg, (screen_width, screen_height)).convert_alpha()

# Snake images
snake_head = pygame.image.load("snake_head.png")
snake_body = pygame.image.load("snake_body.png")

snake_size = 20
snake_head = pygame.transform.scale(snake_head, (snake_size, snake_size))
snake_body = pygame.transform.scale(snake_body, (snake_size, snake_size))

pygame.display.set_caption("Snake Game")
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def rotated_head(direction):
    if direction == "UP":
        return pygame.transform.rotate(snake_head, 90)
    elif direction == "DOWN":
        return pygame.transform.rotate(snake_head, 270)
    elif direction == "LEFT":
        return pygame.transform.rotate(snake_head, 180)
    else:
        return snake_head

def plot_snake(gameWindow, snk_list, direction):
    for i, (x, y) in enumerate(snk_list):
        if i == len(snk_list) - 1:  # head
            gameWindow.blit(rotated_head(direction), (x, y))
        else:
            gameWindow.blit(snake_body, (x, y))

def welcome_screen():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233, 220, 229))
        gameWindow.blit(welbgimg, (0, 0))
        text_screen("Welcome to Snake Game.", black, 210, 400)
        text_screen("Press 'Space' To Play.", black, 240, 440)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
        pygame.display.update()
        clock.tick(60)

def game_loop():

    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 5
    velocity_y = 0
    direction = "RIGHT"

    food_x = random.randint(20, screen_width - 40)
    food_y = random.randint(20, screen_height - 40)
    score = 0
    init_velocity = 5
    fps = 60
    snk_list = []
    snk_length = 1

    # High score file handling
    if not os.path.exists("High_score.txt"):
        with open("High_score.txt", "w") as f:
            f.write("0")

    with open("High_score.txt", 'r') as f:
        highscore = int(f.read())

    while not exit_game:
        if game_over:
            with open("High_score.txt", 'w') as f:
                f.write(str(highscore))

            gameWindow.fill(white)
            text_screen("Game Over! Press Enter to Continue", red, 80, 250)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:

                    # Prevent opposite direction turns
                    if event.key == pygame.K_RIGHT and direction != "LEFT":
                        velocity_x = init_velocity
                        velocity_y = 0
                        direction = "RIGHT"

                    if event.key == pygame.K_LEFT and direction != "RIGHT":
                        velocity_x = -init_velocity
                        velocity_y = 0
                        direction = "LEFT"

                    if event.key == pygame.K_UP and direction != "DOWN":
                        velocity_y = -init_velocity
                        velocity_x = 0
                        direction = "UP"

                    if event.key == pygame.K_DOWN and direction != "UP":
                        velocity_y = init_velocity
                        velocity_x = 0
                        direction = "DOWN"

            snake_x += velocity_x
            snake_y += velocity_y

            # Eating food
            if abs(snake_x - food_x) < 15 and abs(snake_y - food_y) < 15:
                pygame.mixer.music.load("snake-game-food.mp3")
                pygame.mixer.music.play()
                score += 1
                food_x = random.randint(20, screen_width - 40)
                food_y = random.randint(20, screen_height - 40)
                snk_length += 5
                if score > highscore:
                    highscore = score

            gameWindow.fill(black)
            gameWindow.blit(bgimg, (0, 0))
            text_screen(f"Score: {score}  High Score: {highscore}", red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = [snake_x, snake_y]
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            # Collision with body
            if head in snk_list[:-1]:
                pygame.mixer.music.load("snake-game-over.mp3")
                pygame.mixer.music.play()
                game_over = True

            # Border collision
            if snake_x < 0 or snake_y < 0 or snake_x > screen_width - snake_size or snake_y > screen_height - snake_size:
                pygame.mixer.music.load("snake-game-over.mp3")
                pygame.mixer.music.play()
                game_over = True

            plot_snake(gameWindow, snk_list, direction)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome_screen()
