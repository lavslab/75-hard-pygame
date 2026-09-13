import pygame

# start pygame
pygame.init()

# ---------------- GAME WINDOW ----------------

WIDTH = 900
HEIGHT = 500

# the whole level is wider than the screen
WORLD_WIDTH = 3000

# colors
PINK = (255, 220, 235)
DARK_PINK = (210, 80, 140)

# create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("75 Hard: Lav Edition")

# clock
clock = pygame.time.Clock()

# font
font = pygame.font.Font(None, 36)


# ---------------- PLAYER IMAGES ----------------

lav_width = 70
lav_height = 100

# front-facing idle image
lav_image = pygame.image.load(
    "assets/lav_idle.png"
).convert_alpha()

lav_image = pygame.transform.scale(
    lav_image,
    (lav_width, lav_height)
)

# running frames
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

run_frames = [
    pygame.transform.scale(frame, (lav_width, lav_height))
    for frame in run_frames
]

# jumping frames
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

jump_frames = [
    pygame.transform.scale(frame, (lav_width, lav_height))
    for frame in jump_frames
]


# ---------------- WATER IMAGE ----------------

water_width = 45
water_height = 70

water_image = pygame.image.load(
    "assets/water_bottle.png"
).convert_alpha()

water_image = pygame.transform.scale(
    water_image,
    (water_width, water_height)
)


# ---------------- PLAYER SETTINGS ----------------

# Lav's position inside the WORLD
lav_x = 100
lav_y = 350

lav_speed = 5

# jumping
lav_y_velocity = 0
gravity = 1
jump_strength = -15


# ---------------- ANIMATION ----------------

run_animation_index = 0
run_animation_speed = 0.15

jump_animation_index = 0
jump_animation_speed = 0.12


# ---------------- WATER COLLECTIBLE ----------------

# this is now the bottle's WORLD position
water_x = 650
water_y = 380

water_collected = False

water_count = 0
water_goal = 5


# ---------------- CAMERA ----------------

camera_x = 0


# ---------------- MAIN GAME LOOP ----------------

running = True

while running:

    # close game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # keyboard input
    keys = pygame.key.get_pressed()


    # ---------------- MOVEMENT ----------------

    # move left through the world
    if keys[pygame.K_LEFT] and lav_x > 0:
        lav_x -= lav_speed

    # move right through the world
    if keys[pygame.K_RIGHT] and lav_x < WORLD_WIDTH - lav_width:
        lav_x += lav_speed


    # ---------------- RUNNING ANIMATION ----------------

    if (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]) and lav_y == 350:

        run_animation_index += run_animation_speed

        if run_animation_index >= len(run_frames):
            run_animation_index = 0

    else:
        run_animation_index = 0


    # ---------------- JUMP ----------------

    if keys[pygame.K_SPACE] and lav_y == 350:
        lav_y_velocity = jump_strength

    # gravity
    lav_y_velocity += gravity
    lav_y += lav_y_velocity

    # keep Lav on the ground
    if lav_y >= 350:
        lav_y = 350
        lav_y_velocity = 0


    # ---------------- JUMP ANIMATION ----------------

    if lav_y < 350:

        jump_animation_index += jump_animation_speed

        if jump_animation_index >= len(jump_frames):
            jump_animation_index = len(jump_frames) - 1

    else:
        jump_animation_index = 0


    # ---------------- CAMERA ----------------

    # camera follows Lav once she moves toward the middle
    camera_x = lav_x - WIDTH // 2

    # don't let camera go past beginning of world
    if camera_x < 0:
        camera_x = 0

    # don't let camera go past end of world
    if camera_x > WORLD_WIDTH - WIDTH:
        camera_x = WORLD_WIDTH - WIDTH


    # ---------------- COLLISION ----------------

    # collision uses WORLD positions
    lav_rect = pygame.Rect(
        lav_x,
        lav_y,
        lav_width,
        lav_height
    )

    water_rect = pygame.Rect(
        water_x,
        water_y,
        water_width,
        water_height
    )

    # collect bottle
    if not water_collected and lav_rect.colliderect(water_rect):
        water_collected = True
        water_count += 1


    # ---------------- SCREEN POSITIONS ----------------

    # convert world positions into screen positions
    lav_screen_x = lav_x - camera_x
    water_screen_x = water_x - camera_x


    # ---------------- DRAW EVERYTHING ----------------

    # background
    screen.fill(PINK)

    # ground
    pygame.draw.rect(
        screen,
        DARK_PINK,
        (0, 450, WIDTH, 50)
    )


    # ---------------- DRAW WATER ----------------

    if not water_collected:

        screen.blit(
            water_image,
            (water_screen_x, water_y)
        )


    # ---------------- DRAW LAV ----------------

    if lav_y < 350:

        # jumping
        current_frame = jump_frames[int(jump_animation_index)]

        screen.blit(
            current_frame,
            (lav_screen_x, lav_y)
        )

    elif keys[pygame.K_RIGHT]:

        # running right
        current_frame = run_frames[int(run_animation_index)]

        screen.blit(
            current_frame,
            (lav_screen_x, lav_y)
        )

    elif keys[pygame.K_LEFT]:

        # running left
        current_frame = run_frames[int(run_animation_index)]

        current_frame = pygame.transform.flip(
            current_frame,
            True,
            False
        )

        screen.blit(
            current_frame,
            (lav_screen_x, lav_y)
        )

    else:

        # standing still
        screen.blit(
            lav_image,
            (lav_screen_x, lav_y)
        )


    # ---------------- WATER COUNTER ----------------

    water_text = font.render(
        f"Water: {water_count}/{water_goal}",
        True,
        DARK_PINK
    )

    screen.blit(
        water_text,
        (20, 20)
    )


    # show finished frame
    pygame.display.update()

    # 60 FPS
    clock.tick(60)


pygame.quit()