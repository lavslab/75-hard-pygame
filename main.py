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

# player size
lav_width = 70
lav_height = 100

# load front-facing player image
lav_image = pygame.image.load(
    "assets/lav_idle.png"
).convert_alpha()

lav_image = pygame.transform.scale(
    lav_image,
    (lav_width, lav_height)
)

# load running frames
run_frames = [
    pygame.image.load(
        "assets/lav_sprite_frames/game_ready/run_right/run_right_1.png"
    ).convert_alpha(),

    pygame.image.load(
        "assets/lav_sprite_frames/game_ready/run_right/run_right_2.png"
    ).convert_alpha(),

    pygame.image.load(
        "assets/lav_sprite_frames/game_ready/run_right/run_right_3.png"
    ).convert_alpha(),

    pygame.image.load(
        "assets/lav_sprite_frames/game_ready/run_right/run_right_4.png"
    ).convert_alpha(),
]

# resize running frames
run_frames = [
    pygame.transform.scale(frame, (lav_width, lav_height))
    for frame in run_frames
]

# load jumping frames
jump_frames = [
    pygame.image.load(
        "assets/lav_sprite_frames/game_ready/jump/jump_1.png"
    ).convert_alpha(),

    pygame.image.load(
        "assets/lav_sprite_frames/game_ready/jump/jump_2.png"
    ).convert_alpha(),

    pygame.image.load(
        "assets/lav_sprite_frames/game_ready/jump/jump_3.png"
    ).convert_alpha(),
]

# resize jumping frames
jump_frames = [
    pygame.transform.scale(frame, (lav_width, lav_height))
    for frame in jump_frames
]

# load water bottle
water_image = pygame.image.load(
    "assets/water_bottle.png"
).convert_alpha()

water_image = pygame.transform.scale(
    water_image,
    (45, 70)
)

# clock
clock = pygame.time.Clock()

# player settings
lav_x = 100
lav_y = 350
lav_speed = 5

# water bottle position
water_x = 650
water_y = 380

# jumping settings
lav_y_velocity = 0
gravity = 1
jump_strength = -15

# animation settings
run_animation_index = 0
run_animation_speed = 0.15

jump_animation_index = 0
jump_animation_speed = 0.12

# ------ main game loop ------
running = True

while running:

    # close game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # get keyboard input
    keys = pygame.key.get_pressed()

    # move left
    if keys[pygame.K_LEFT] and lav_x > 0:
        lav_x -= lav_speed

    # move right
    if keys[pygame.K_RIGHT] and lav_x < WIDTH - lav_width:
        lav_x += lav_speed

    # running animation
    if (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]) and lav_y == 350:
        run_animation_index += run_animation_speed

        # restart animation after the last frame
        if run_animation_index >= len(run_frames):
            run_animation_index = 0

    else:
        run_animation_index = 0

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

    # jump animation
    if lav_y < 350:
        jump_animation_index += jump_animation_speed

        if jump_animation_index >= len(jump_frames):
            jump_animation_index = len(jump_frames) - 1

    else:
        jump_animation_index = 0

    # ---------------- DRAW EVERYTHING ----------------

    # pink background
    screen.fill(PINK)

    # ground
    pygame.draw.rect(
        screen,
        DARK_PINK,
        (0, 450, WIDTH, 50)
    )

    # draw Lav
    if lav_y < 350:
        # Lav is jumping
        current_frame = jump_frames[int(jump_animation_index)]
        screen.blit(current_frame, (lav_x, lav_y))

    elif keys[pygame.K_RIGHT]:
        # Lav is running right
        current_frame = run_frames[int(run_animation_index)]
        screen.blit(current_frame, (lav_x, lav_y))

    elif keys[pygame.K_LEFT]:
        # get the same running frame
        current_frame = run_frames[int(run_animation_index)]

        # flip it horizontally so Lav faces left
        current_frame = pygame.transform.flip(
            current_frame,
            True,
            False
        )

        screen.blit(current_frame, (lav_x, lav_y))

    else:
        # Lav is standing still
        screen.blit(lav_image, (lav_x, lav_y))

        # draw water bottle
        screen.blit(water_image, (water_x, water_y))

        

    # show finished frame
    pygame.display.update()

    # keep game running at 60 FPS
    clock.tick(60)

pygame.quit()