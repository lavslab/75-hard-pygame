import pygame

pygame.init()

# ---------------- GAME WINDOW ----------------

WIDTH = 900
HEIGHT = 500
WORLD_WIDTH = 3000

DARK_PINK = (210, 80, 140)
WHITE = (255, 255, 255)
RED = (220, 50, 70)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("75 Hard: Lav Edition")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)


# ---------------- BACKGROUND ----------------

background_image = pygame.image.load(
    "assets/background.png"
).convert()

background_image = pygame.transform.scale(
    background_image,
    (WIDTH, HEIGHT)
)


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


# ---------------- RUNNING FRAMES ----------------

run_frames = [
    pygame.image.load(
        f"assets/lav_sprite_frames/game_ready/run_right/run_right_{i}.png"
    ).convert_alpha()
    for i in range(1, 5)
]

run_frames = [
    pygame.transform.scale(
        frame,
        (lav_width, lav_height)
    )
    for frame in run_frames
]


# ---------------- JUMPING FRAMES ----------------

jump_frames = [
    pygame.image.load(
        f"assets/lav_sprite_frames/game_ready/jump/jump_{i}.png"
    ).convert_alpha()
    for i in range(1, 4)
]

jump_frames = [
    pygame.transform.scale(
        frame,
        (lav_width, lav_height)
    )
    for frame in jump_frames
]


# ---------------- WATER IMAGE ----------------

water_width = 40
water_height = 65

water_image = pygame.image.load(
    "assets/water_bottle.png"
).convert_alpha()

water_image = pygame.transform.scale(
    water_image,
    (water_width, water_height)
)


# ---------------- WATER SOUND ----------------

try:
    water_ding = pygame.mixer.Sound(
        "assets/water_ding.wav"
    )

except (pygame.error, FileNotFoundError):
    water_ding = None
    print("water_ding.wav not found - continuing without sound")


# ---------------- JUNK FOOD IMAGE ----------------

junk_width = 90
junk_height = 60

junk_image = pygame.image.load(
    "assets/junk_food.png"
).convert_alpha()

junk_image = pygame.transform.scale(
    junk_image,
    (junk_width, junk_height)
)


# ---------------- JUNK FOOD SOUND ----------------

try:
    junk_food_sound = pygame.mixer.Sound(
        "assets/junk_food_hit.wav"
    )

except (pygame.error, FileNotFoundError):
    junk_food_sound = None
    print("junk_food_hit.wav not found - continuing without sound")


# ---------------- PLAYER SETTINGS ----------------

lav_x = 100
lav_y = 350
lav_speed = 5

lav_y_velocity = 0
gravity = 1

# slightly stronger jump
jump_strength = -16


# ---------------- ANIMATION ----------------

run_animation_index = 0
run_animation_speed = 0.15

jump_animation_index = 0
jump_animation_speed = 0.12


# ---------------- WATER BOTTLES ----------------

# bottle 1
water_1_x = 650
water_1_y = 385
water_1_collected = False

# bottle 2
water_2_x = 1200
water_2_y = 385
water_2_collected = False

water_count = 0
water_goal = 5


# ---------------- WATER PICKUP POPUP ----------------

water_popup_timer = 0
water_popup_y = 0


# ---------------- JUNK FOOD OBSTACLE ----------------

junk_x = 900
junk_y = 390

# floating red warning
junk_message_timer = 0
junk_popup_y = 0

# prevents collision from triggering every frame
junk_collision_cooldown = 0


# ---------------- CAMERA ----------------

camera_x = 0


# ---------------- MAIN GAME LOOP ----------------

running = True

while running:

    # ---------------- EVENTS ----------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


    # ---------------- KEYBOARD ----------------

    keys = pygame.key.get_pressed()


    # ---------------- MOVEMENT ----------------

    if keys[pygame.K_LEFT] and lav_x > 0:
        lav_x -= lav_speed

    if keys[pygame.K_RIGHT] and lav_x < WORLD_WIDTH - lav_width:
        lav_x += lav_speed


    # ---------------- RUNNING ANIMATION ----------------

    if (
        (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT])
        and lav_y == 350
    ):

        run_animation_index += run_animation_speed

        if run_animation_index >= len(run_frames):
            run_animation_index = 0

    else:
        run_animation_index = 0


    # ---------------- JUMP ----------------

    if keys[pygame.K_SPACE] and lav_y == 350:
        lav_y_velocity = jump_strength


    # ---------------- GRAVITY ----------------

    lav_y_velocity += gravity
    lav_y += lav_y_velocity

    # keep Lav on ground
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

    camera_x = lav_x - WIDTH // 2

    camera_x = max(
        0,
        min(camera_x, WORLD_WIDTH - WIDTH)
    )


    # ---------------- COLLISION RECTS ----------------

    # smaller Lav hitbox
    lav_rect = pygame.Rect(
        lav_x + 15,
        lav_y + 20,
        40,
        75
    )

    # bottle 1
    water_1_rect = pygame.Rect(
        water_1_x,
        water_1_y,
        water_width,
        water_height
    )

    # bottle 2
    water_2_rect = pygame.Rect(
        water_2_x,
        water_2_y,
        water_width,
        water_height
    )

    # smaller junk-food hitbox
    junk_rect = pygame.Rect(
        junk_x + 20,
        junk_y + 25,
        50,
        30
    )


    # ---------------- WATER COLLISION ----------------

    # bottle 1
    if (
        not water_1_collected
        and lav_rect.colliderect(water_1_rect)
    ):

        water_1_collected = True
        water_count += 1

        # floating +1 WATER
        water_popup_timer = 60
        water_popup_y = lav_y - 10

        # play ding
        if water_ding:
            water_ding.play()


    # bottle 2
    if (
        not water_2_collected
        and lav_rect.colliderect(water_2_rect)
    ):

        water_2_collected = True
        water_count += 1

        # floating +1 WATER
        water_popup_timer = 60
        water_popup_y = lav_y - 10

        # play ding
        if water_ding:
            water_ding.play()


    # ---------------- JUNK FOOD COLLISION ----------------

    if junk_collision_cooldown > 0:
        junk_collision_cooldown -= 1


    if (
        lav_rect.colliderect(junk_rect)
        and junk_collision_cooldown == 0
    ):

        # floating red warning
        junk_message_timer = 60
        junk_popup_y = lav_y - 10

        # play error sound
        if junk_food_sound:
            junk_food_sound.play()

        # bump Lav backwards
        lav_x -= 80

        # don't let her leave the world
        lav_x = max(0, lav_x)

        # prevent repeated instant collisions
        junk_collision_cooldown = 30

        print("Oops! Junk food!")


    # ---------------- SCREEN POSITIONS ----------------

    lav_screen_x = lav_x - camera_x

    water_1_screen_x = water_1_x - camera_x
    water_2_screen_x = water_2_x - camera_x

    junk_screen_x = junk_x - camera_x


    # ---------------- DRAW BACKGROUND ----------------

    background_offset = camera_x % WIDTH

    screen.blit(
        background_image,
        (-background_offset, 0)
    )

    screen.blit(
        background_image,
        (WIDTH - background_offset, 0)
    )


    # ---------------- DRAW WATER ----------------

    if not water_1_collected:

        screen.blit(
            water_image,
            (water_1_screen_x, water_1_y)
        )


    if not water_2_collected:

        screen.blit(
            water_image,
            (water_2_screen_x, water_2_y)
        )


    # ---------------- DRAW JUNK FOOD ----------------

    screen.blit(
        junk_image,
        (junk_screen_x, junk_y)
    )


    # ---------------- DRAW LAV ----------------

    if lav_y < 350:

        # jumping
        current_frame = jump_frames[
            int(jump_animation_index)
        ]

        screen.blit(
            current_frame,
            (lav_screen_x, lav_y)
        )


    elif keys[pygame.K_RIGHT]:

        # running right
        current_frame = run_frames[
            int(run_animation_index)
        ]

        screen.blit(
            current_frame,
            (lav_screen_x, lav_y)
        )


    elif keys[pygame.K_LEFT]:

        # running left
        current_frame = run_frames[
            int(run_animation_index)
        ]

        # flip sprite to face left
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

        # standing still / facing forward
        screen.blit(
            lav_image,
            (lav_screen_x, lav_y)
        )


    # ---------------- WATER PICKUP POPUP ----------------

    if water_popup_timer > 0:

        pickup_text = font.render(
            "+1 WATER!",
            True,
            WHITE
        )

        popup_x = (
            lav_screen_x
            + lav_width // 2
            - pickup_text.get_width() // 2
        )

        screen.blit(
            pickup_text,
            (popup_x, water_popup_y)
        )

        # float upward
        water_popup_y -= 0.5

        water_popup_timer -= 1


    # ---------------- JUNK FOOD POPUP ----------------

    if junk_message_timer > 0:

        junk_text = font.render(
            "! JUNK FOOD !",
            True,
            RED
        )

        junk_popup_x = (
            lav_screen_x
            + lav_width // 2
            - junk_text.get_width() // 2
        )

        screen.blit(
            junk_text,
            (junk_popup_x, junk_popup_y)
        )

        # float upward
        junk_popup_y -= 0.5

        junk_message_timer -= 1


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


    # ---------------- UPDATE SCREEN ----------------

    pygame.display.update()

    clock.tick(60)


pygame.quit()