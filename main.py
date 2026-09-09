import pygame

# start pygame
pygame.init()

# game window size
WIDTH = 900
HEIGHT = 500

# colors
PINK = (255, 220, 235)
DARK_PINK = (210, 80, 140)

# create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("75 Hard: Lav Edition")

# load player image
lav_image = pygame.image.load("assets/lav_idle.png").convert_alpha()

# resize player image
lav_image = pygame.transform.scale(lav_image, (70, 100))

# add time clock
clock = pygame.time.Clock()

# player settings
lav_x = 100
lav_y = 350
lav_width = 70
lav_height = 100
lav_speed = 5

# jumping settings
lav_y_velocity = 0
gravity = 1
jump_strength = -15

# ------ main game loop ------
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # player movement
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and lav_x > 0:
        lav_x -= lav_speed

    if keys[pygame.K_RIGHT] and lav_x < WIDTH - lav_width:
        lav_x += lav_speed

    # jump
    if keys[pygame.K_SPACE] and lav_y == 350:
        lav_y_velocity = jump_strength

    # gravity
    lav_y_velocity += gravity
    lav_y += lav_y_velocity

    # keep Lav on the ground
    if lav_y >= 350:
        lav_y = 350
        lav_y_velocity = 0

    # pink background screen
    screen.fill(PINK)

    # ground
    pygame.draw.rect(
        screen,
        DARK_PINK,
        (0, 450, WIDTH, 50)
    )

    # draw player
    screen.blit(lav_image, (lav_x, lav_y))

    # update after each drawing aka finished frame
    pygame.display.update()

    # keep game running at 60 FPS
    clock.tick(60)

pygame.quit()