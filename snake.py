import pygame
import random

# Initialize pygame
pygame.init()

# Set up the display
width, height = 1600, 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Snake attributes
block_size = 10
initial_snake_speed = 5
max_snake_speed = 100
snake_speed_increment = 5

# Font
font = pygame.font.SysFont(None, 30)

# List of background colors for different level ranges
level_colors = [
    (0, 0, 0),        # Level 1-5
    (46, 41, 0),     # Level 6-10
    (0, 74, 0),     # Level 11-15
    (0, 0, 90),     # Level 16-20
    (66, 0, 66),    # Level 21-25
    (110, 53, 24),   # Level 26-30
    (20, 46, 71)   # Level 31-35
]

# Function to draw text on screen
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Function to draw the snake
def draw_snake(block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], block_size, block_size])

# Pause function
def pause_game():
    paused = True
    while paused:
        screen.fill(BLACK)
        draw_text("Paused. Press P to resume or Q to quit", font, WHITE, screen, width/4, height/3)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False  # Resume the game
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Function to display the game
def gameLoop():
    game_over = False
    game_close = False
    level = 1
    food_eaten = 0

    # Initial position of the snake
    x = width / 2
    y = height / 2

    # Initial velocity of the snake
    x_change = 0
    y_change = 0

    # Snake body
    snake_list = []
    snake_length = 1

    # Initial position of the food
    food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
    food_y = round(random.randrange(0, height - block_size) / block_size) * block_size
    
    # Set initial snake speed
    snake_speed = initial_snake_speed  

    clock = pygame.time.Clock()

    while not game_over:

        while game_close == True:
            screen.fill(BLACK)
            draw_text("You lost! Press Q to quit or C to play again", font, RED, screen, width/4, height/3)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -block_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = block_size
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -block_size
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = block_size
                    x_change = 0
                elif event.key == pygame.K_p:
                    pause_game()  # Call the pause function
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    game_over = True  # Quit the game when Q or ESC is pressed

        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True
        x += x_change
        y += y_change

        # Determine the background color based on the level
        color_index = (level - 1) // 5  # Change color every 5 levels
        current_color = level_colors[color_index % len(level_colors)]
        screen.fill(current_color)  # Set background color based on level
        
        pygame.draw.rect(screen, RED, [food_x, food_y, block_size, block_size])
        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(block_size, snake_list)

        # Display food count and current level
        draw_text("Food eaten: " + str(food_eaten), font, WHITE, screen, 10,10) 
        draw_text("Level: " + str(level), font, WHITE, screen, width - 120, 10)

        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
            food_y = round(random.randrange(0, height - block_size) / block_size) * block_size
            snake_length += 1
            food_eaten += 1

            # Increase level and speed every 10 food items
            if food_eaten % 10 == 0:
                level += 1
                snake_speed += snake_speed_increment  # Increase snake speed
                if snake_speed > max_snake_speed:  # Limit maximum speed
                    snake_speed = max_snake_speed

        clock.tick(snake_speed)  # Update snake speed

    pygame.quit()
    quit()

gameLoop()
