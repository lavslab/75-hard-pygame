import pygame

# start pygame
pygame.init()

# game window size
WIDTH = 900
HEIGHT = 500

# colors
PINK = (255, 220, 235)
HOT_PINK = (255, 105, 180)
DARK_PINK = (210, 80, 140)

#create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("75 Hard: Lav Edition")

# add time clock
clock = pygame.time.Clock()

# player settings
lav_x = 100
lav_y = 380
lav_width = 50
lav_height = 70
lav_speed = 5


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

# pink background screen
    screen.fill(PINK)

# ground
    pygame.draw.rect(screen, DARK_PINK, (0, 450, WIDTH, 50))

    
# draw player
    pygame.draw.rect(
        screen,
        (255, 105, 180),
        (lav_x, lav_y, lav_width, lav_height)
    )

    # update after each drawing aka finished frame
    pygame.display.update()

clock.tick(60)
pygame.quit()