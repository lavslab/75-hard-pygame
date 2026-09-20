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
small_font = pygame.font.Font(None, 30)
hud_title_font = pygame.font.Font(None, 30)
hud_font = pygame.font.Font(None, 25)


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


# ---------------- READING FRAMES ----------------

read_frames = [
    pygame.image.load(
        f"assets/lav_sprite_frames/game_ready/read/read_{i}.png"
    ).convert_alpha()
    for i in range(1, 5)
]

read_frames = [
    pygame.transform.scale(frame, (lav_width, lav_height))
    for frame in read_frames
]


# ---------------- DRINKING FRAMES ----------------

drink_frames = [
    pygame.image.load(
        f"assets/lav_sprite_frames/game_ready/drink/drink_{i}.png"
    ).convert_alpha()
    for i in range(1, 5)
]

drink_frames = [
    pygame.transform.scale(frame, (lav_width, lav_height))
    for frame in drink_frames
]


# ---------------- WORKOUT FRAMES ----------------
workout_frames = [
    pygame.image.load(f"assets/lav_sprite_frames/game_ready/workout/workout_{i}.png").convert_alpha()
    for i in range(1, 5)
]
workout_frames = [pygame.transform.scale(frame, (lav_width, lav_height)) for frame in workout_frames]

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


# ---------------- BOOK IMAGE ----------------

book_width = 75
book_height = 65

book_image = pygame.image.load(
    "assets/book.png"
).convert_alpha()

book_image = pygame.transform.scale(
    book_image,
    (book_width, book_height)
)


# ---------------- BOOK SOUND ----------------

try:
    book_read_sound = pygame.mixer.Sound(
        "assets/book_read.wav"
    )

except (pygame.error, FileNotFoundError):
    book_read_sound = None
    print("book_read.wav not found - continuing without sound")


# ---------------- DUMBBELL IMAGE ----------------

dumbbell_width = 85
dumbbell_height = 55

dumbbell_image = pygame.image.load(
    "assets/dumbbell.png"
).convert_alpha()

dumbbell_image = pygame.transform.scale(
    dumbbell_image,
    (dumbbell_width, dumbbell_height)
)


# ---------------- PLAYER SETTINGS ----------------

lav_x = 100
lav_y = 350
lav_speed = 5

lav_y_velocity = 0
gravity = 1
jump_strength = -16


# ---------------- ANIMATION ----------------

run_animation_index = 0
run_animation_speed = 0.15

jump_animation_index = 0
jump_animation_speed = 0.12


# ---------------- WATER BOTTLES ----------------

water_bottles = [
    {"x": 650, "y": 385, "collected": False},
    {"x": 1200, "y": 385, "collected": False},
    {"x": 1600, "y": 385, "collected": False},
    {"x": 2050, "y": 385, "collected": False},
    {"x": 2550, "y": 385, "collected": False},
]

water_count = 0
water_goal = 5


# ---------------- WATER POPUP ----------------

water_popup_timer = 0
water_popup_y = 0

# Drinking animation state
drinking_active = False
drink_animation_index = 0.0
drink_animation_speed = 0.10
current_water_bottle = None


# ---------------- JUNK FOOD ----------------

junk_x = 900
junk_y = 390

junk_message_timer = 0
junk_popup_y = 0

junk_collision_cooldown = 0


# ---------------- BOOK / READING CHALLENGE ----------------

# Book appears between water bottle 3 and 4
book_x = 1825
book_y = 385

book_read = False

# how close Lav needs to be before R prompt appears
book_interaction_distance = 100

# floating completion message
book_popup_timer = 0
book_popup_y = 0

# Reading animation state
reading_active = False
read_animation_index = 0.0
read_animation_speed = 0.035



# ---------------- WORKOUT CHALLENGE ----------------

dumbbell_x = 2250
dumbbell_y = 395
workout_interaction_distance = 110

workout_active = False
workout_complete = False
workout_reps = 0
workout_goal = 10

workout_popup_timer = 0
workout_popup_y = 0
workout_rep_animating = False
workout_animation_index = 0.0
workout_animation_speed = 0.18


# ---------------- CAMERA ----------------

camera_x = 0


# ---------------- MAIN GAME LOOP ----------------

running = True

while running:

    # ---------------- EVENTS ----------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


        # ---------------- INTERACTIONS ----------------

        if event.type == pygame.KEYDOWN:

            # Read book with R
            if event.key == pygame.K_r and not book_read and not reading_active and not workout_active and not drinking_active:

                lav_center = lav_x + lav_width // 2
                book_center = book_x + book_width // 2

                distance_to_book = abs(
                    lav_center - book_center
                )

                if distance_to_book <= book_interaction_distance:

                    reading_active = True
                    read_animation_index = 0.0
                    lav_y_velocity = 0

                    if book_read_sound:
                        book_read_sound.play()

                    print("Reading started!")

            # Start workout with W
            if event.key == pygame.K_w and not workout_complete and not workout_active and not drinking_active and not reading_active:

                lav_center = lav_x + lav_width // 2
                dumbbell_center = dumbbell_x + dumbbell_width // 2

                distance_to_dumbbell = abs(
                    lav_center - dumbbell_center
                )

                if distance_to_dumbbell <= workout_interaction_distance:
                    workout_active = True
                    workout_reps = 0
                    print("Workout started!")

            # One SPACE press starts one complete animated curl.
            elif event.key == pygame.K_SPACE and workout_active and not workout_rep_animating:
                workout_rep_animating = True
                workout_animation_index = 0.0



    # ---------------- KEYBOARD ----------------

    keys = pygame.key.get_pressed()


    # ---------------- MOVEMENT ----------------

    if not workout_active and not drinking_active and not reading_active:

        if keys[pygame.K_LEFT] and lav_x > 0:
            lav_x -= lav_speed

        if keys[pygame.K_RIGHT] and lav_x < WORLD_WIDTH - lav_width:
            lav_x += lav_speed


    # ---------------- RUNNING ANIMATION ----------------

    if (
        (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT])
        and lav_y == 350
        and not drinking_active
        and not reading_active
    ):

        run_animation_index += run_animation_speed

        if run_animation_index >= len(run_frames):
            run_animation_index = 0

    else:
        run_animation_index = 0


    # ---------------- JUMP ----------------

    if (
        keys[pygame.K_SPACE]
        and lav_y == 350
        and not workout_active
        and not drinking_active
        and not reading_active
    ):
        lav_y_velocity = jump_strength


    # ---------------- GRAVITY ----------------

    lav_y_velocity += gravity
    lav_y += lav_y_velocity

    if lav_y >= 350:
        lav_y = 350
        lav_y_velocity = 0


    # ---------------- JUMP ANIMATION ----------------
    if lav_y < 350 and not workout_active and not drinking_active and not reading_active:
        jump_animation_index += jump_animation_speed
        if jump_animation_index >= len(jump_frames):
            jump_animation_index = len(jump_frames) - 1
    else:
        jump_animation_index = 0

    # ---------------- WORKOUT ANIMATION ----------------
    if workout_active and workout_rep_animating:
        workout_animation_index += workout_animation_speed
        if workout_animation_index >= len(workout_frames):
            workout_rep_animating = False
            workout_animation_index = 0.0
            workout_reps += 1
            print(f"Rep {workout_reps}/{workout_goal}")
            if workout_reps >= workout_goal:
                workout_reps = workout_goal
                workout_active = False
                workout_complete = True
                workout_popup_timer = 90
                workout_popup_y = lav_y - 10
                print("Workout complete!")

    # ---------------- DRINKING ANIMATION ----------------

    if drinking_active:

        drink_animation_index += drink_animation_speed

        # Once all 4 drinking frames finish, collect the bottle.
        if drink_animation_index >= len(drink_frames):

            drinking_active = False
            drink_animation_index = 0.0

            if current_water_bottle is not None:
                current_water_bottle["collected"] = True
                water_count += 1

                water_popup_timer = 60
                water_popup_y = lav_y - 10

                if water_ding:
                    water_ding.play()

                print(f"Water {water_count}/{water_goal}")

                current_water_bottle = None


    # ---------------- READING ANIMATION ----------------

    if reading_active:

        read_animation_index += read_animation_speed

        if read_animation_index >= len(read_frames):

            reading_active = False
            read_animation_index = 0.0
            book_read = True

            book_popup_timer = 90
            book_popup_y = lav_y - 10

            print("10 pages complete!")


    # ---------------- CAMERA ----------------

    camera_x = lav_x - WIDTH // 2

    camera_x = max(
        0,
        min(camera_x, WORLD_WIDTH - WIDTH)
    )


    # ---------------- COLLISION RECTS ----------------

    lav_rect = pygame.Rect(
        lav_x + 15,
        lav_y + 20,
        40,
        75
    )

    junk_rect = pygame.Rect(
        junk_x + 20,
        junk_y + 25,
        50,
        30
    )


    # ---------------- WATER COLLISION ----------------

    # Touching a bottle starts the drinking animation.
    # The bottle is only counted/disappears AFTER the animation finishes.
    if not drinking_active and not workout_active and not reading_active:

        for bottle in water_bottles:

            bottle_rect = pygame.Rect(
                bottle["x"],
                bottle["y"],
                water_width,
                water_height
            )

            if (
                not bottle["collected"]
                and lav_rect.colliderect(bottle_rect)
            ):
                drinking_active = True
                drink_animation_index = 0.0
                current_water_bottle = bottle
                lav_y_velocity = 0
                break


    # ---------------- JUNK FOOD COLLISION ----------------

    if junk_collision_cooldown > 0:
        junk_collision_cooldown -= 1


    if (
        lav_rect.colliderect(junk_rect)
        and junk_collision_cooldown == 0
        and not drinking_active
        and not reading_active
    ):

        junk_message_timer = 60
        junk_popup_y = lav_y - 10

        if junk_food_sound:
            junk_food_sound.play()

        lav_x -= 80
        lav_x = max(0, lav_x)

        junk_collision_cooldown = 30

        print("Oops! Junk food!")


    # ---------------- BOOK DISTANCE ----------------

    lav_center = lav_x + lav_width // 2
    book_center = book_x + book_width // 2

    distance_to_book = abs(
        lav_center - book_center
    )

    near_book = (
        distance_to_book <= book_interaction_distance
        and not book_read
        and not drinking_active
        and not reading_active
    )


    # ---------------- WORKOUT DISTANCE ----------------

    dumbbell_center = dumbbell_x + dumbbell_width // 2

    distance_to_dumbbell = abs(
        lav_center - dumbbell_center
    )

    near_dumbbell = (
        distance_to_dumbbell <= workout_interaction_distance
        and not workout_complete
        and not workout_active
        and not drinking_active
        and not reading_active
    )


    # ---------------- SCREEN POSITIONS ----------------

    lav_screen_x = lav_x - camera_x
    junk_screen_x = junk_x - camera_x
    book_screen_x = book_x - camera_x
    dumbbell_screen_x = dumbbell_x - camera_x


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

    for bottle in water_bottles:

        if not bottle["collected"]:

            bottle_screen_x = bottle["x"] - camera_x

            screen.blit(
                water_image,
                (bottle_screen_x, bottle["y"])
            )


    # ---------------- DRAW JUNK FOOD ----------------

    screen.blit(
        junk_image,
        (junk_screen_x, junk_y)
    )


    # ---------------- DRAW BOOK ----------------

    # Book disappears once R is pressed successfully
    if not book_read and not reading_active:

        screen.blit(
            book_image,
            (book_screen_x, book_y)
        )


    # ---------------- DRAW DUMBBELL ----------------

    if not workout_complete:

        screen.blit(
            dumbbell_image,
            (dumbbell_screen_x, dumbbell_y)
        )


    # ---------------- DRAW LAV ----------------
    if reading_active:

        frame_number = min(
            int(read_animation_index),
            len(read_frames) - 1
        )

        current_frame = read_frames[frame_number]

        screen.blit(
            current_frame,
            (lav_screen_x, lav_y)
        )

    elif drinking_active:

        frame_number = min(
            int(drink_animation_index),
            len(drink_frames) - 1
        )

        current_frame = drink_frames[frame_number]

        screen.blit(
            current_frame,
            (lav_screen_x, lav_y)
        )

    elif workout_active:
        if workout_rep_animating:
            frame_number = min(int(workout_animation_index), len(workout_frames) - 1)
            current_frame = workout_frames[frame_number]
        else:
            current_frame = workout_frames[0]
        screen.blit(current_frame, (lav_screen_x, lav_y))
    elif lav_y < 350:
        current_frame = jump_frames[int(jump_animation_index)]
        screen.blit(current_frame, (lav_screen_x, lav_y))
    elif keys[pygame.K_RIGHT]:
        current_frame = run_frames[int(run_animation_index)]
        screen.blit(current_frame, (lav_screen_x, lav_y))
    elif keys[pygame.K_LEFT]:
        current_frame = pygame.transform.flip(run_frames[int(run_animation_index)], True, False)
        screen.blit(current_frame, (lav_screen_x, lav_y))
    else:
        screen.blit(lav_image, (lav_screen_x, lav_y))

    # ---------------- PRESS R PROMPT ----------------

    if near_book:

        read_prompt = small_font.render(
            "Press R to Read",
            True,
            WHITE
        )

        prompt_x = (
            book_screen_x
            + book_width // 2
            - read_prompt.get_width() // 2
        )

        screen.blit(
            read_prompt,
            (prompt_x, book_y - 35)
        )


    # ---------------- PRESS W PROMPT ----------------

    if near_dumbbell:

        workout_prompt = small_font.render(
            "Press W to Workout",
            True,
            WHITE
        )

        workout_prompt_x = (
            dumbbell_screen_x
            + dumbbell_width // 2
            - workout_prompt.get_width() // 2
        )

        screen.blit(
            workout_prompt,
            (workout_prompt_x, dumbbell_y - 35)
        )


    # ---------------- WORKOUT MODE ----------------

    if workout_active:

        workout_title = font.render(
            "WORKOUT",
            True,
            WHITE
        )

        rep_text = font.render(
            f"{workout_reps}/{workout_goal} REPS",
            True,
            WHITE
        )

        rep_prompt_text = "CURL..." if workout_rep_animating else "SPACE = 1 REP"
        rep_prompt = small_font.render(
            rep_prompt_text,
            True,
            WHITE
        )

        center_x = WIDTH // 2

        screen.blit(
            workout_title,
            (center_x - workout_title.get_width() // 2, 65)
        )

        screen.blit(
            rep_text,
            (center_x - rep_text.get_width() // 2, 100)
        )

        screen.blit(
            rep_prompt,
            (center_x - rep_prompt.get_width() // 2, 135)
        )


    # ---------------- WORKOUT COMPLETION POPUP ----------------

    if workout_popup_timer > 0:

        workout_text = font.render(
            "WORKOUT COMPLETE!",
            True,
            WHITE
        )

        workout_popup_x = (
            lav_screen_x
            + lav_width // 2
            - workout_text.get_width() // 2
        )

        screen.blit(
            workout_text,
            (workout_popup_x, workout_popup_y)
        )

        workout_popup_y -= 0.5
        workout_popup_timer -= 1


    # ---------------- WATER POPUP ----------------

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

        junk_popup_y -= 0.5
        junk_message_timer -= 1


    # ---------------- BOOK COMPLETION POPUP ----------------

    if book_popup_timer > 0:

        book_text = font.render(
            "10 PAGES COMPLETE!",
            True,
            WHITE
        )

        book_popup_x = (
            lav_screen_x
            + lav_width // 2
            - book_text.get_width() // 2
        )

        screen.blit(
            book_text,
            (book_popup_x, book_popup_y)
        )

        # float upward
        book_popup_y -= 0.5
        book_popup_timer -= 1


    # ---------------- 75 HARD HUD ----------------

    hud_x = 15
    hud_y = 15
    hud_width = 210
    hud_height = 205

    hud_surface = pygame.Surface(
        (hud_width, hud_height),
        pygame.SRCALPHA
    )
    hud_surface.fill((255, 220, 235, 210))
    screen.blit(hud_surface, (hud_x, hud_y))

    hud_title = hud_title_font.render(
        "75 HARD - DAY 1",
        True,
        DARK_PINK
    )
    screen.blit(hud_title, (hud_x + 15, hud_y + 12))

    water_status = f"{water_count}/{water_goal}"

    if book_read:
        read_status = "DONE"
    else:
        read_status = "--"

    if workout_complete:
        workout_status = "DONE"
    elif workout_active:
        workout_status = f"{workout_reps}/{workout_goal}"
    else:
        workout_status = "--"

    tasks = [
        ("WATER", water_status),
        ("READ", read_status),
        ("WORKOUT", workout_status),
        ("OUTDOOR", "--"),
        ("DIET", "--"),
        ("PHOTO", "--"),
    ]

    task_y = hud_y + 50

    for task_name, task_status in tasks:
        task_text = hud_font.render(
            task_name,
            True,
            DARK_PINK
        )
        screen.blit(task_text, (hud_x + 15, task_y))

        status_text = hud_font.render(
            task_status,
            True,
            WHITE
        )
        screen.blit(
            status_text,
            (
                hud_x + hud_width - status_text.get_width() - 15,
                task_y
            )
        )

        task_y += 24


    # ---------------- UPDATE SCREEN ----------------

    pygame.display.update()
    clock.tick(60)


pygame.quit()