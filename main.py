import pygame

pygame.init()

# ============================================================
# 75 HARD: LAV EDITION
# ============================================================

WIDTH = 900
HEIGHT = 500
WORLD_WIDTH = 3000
GROUND_Y = 350
FPS = 60

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

# ============================================================
# ASSET HELPERS
# ============================================================

def load_image(path, size):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, size)


def load_frames(folder, prefix, count, size):
    frames = []

    for i in range(1, count + 1):
        path = f"assets/lav_sprite_frames/game_ready/{folder}/{prefix}_{i}.png"
        frames.append(load_image(path, size))

    return frames


def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except (pygame.error, FileNotFoundError):
        print(f"Sound unavailable: {path}")
        return None


def play_sound(sound):
    if sound:
        sound.play()


def draw_centered(message, y, text_font=font, color=WHITE):
    text = text_font.render(message, True, color)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))


# ============================================================
# BACKGROUND
# ============================================================

background_image = pygame.image.load(
    "assets/background.png"
).convert()

background_image = pygame.transform.scale(
    background_image,
    (WIDTH, HEIGHT)
)

# ============================================================
# LAV SPRITES
# ============================================================

lav_width = 70
lav_height = 100
lav_size = (lav_width, lav_height)

lav_image = load_image("assets/lav_idle.png", lav_size)

run_frames = load_frames(
    "run_right", "run_right", 4, lav_size
)

jump_frames = load_frames(
    "jump", "jump", 3, lav_size
)

drink_frames = load_frames(
    "drink", "drink", 4, lav_size
)

read_frames = load_frames(
    "read", "read", 4, lav_size
)

workout_frames = load_frames(
    "workout", "workout", 4, lav_size
)

photo_frames = load_frames(
    "photo", "photo", 4, lav_size
)

# NEW: Eating animation
# Eating animation — preserve Lav's proportions
eat_frames = []

for i in range(1, 5):
    image = pygame.image.load(
        f"assets/lav_sprite_frames/game_ready/eat/eat_{i}.png"
    ).convert_alpha()

    original_width, original_height = image.get_size()

    new_height = lav_height
    new_width = int(
        original_width * (new_height / original_height)
    )

    image = pygame.transform.scale(
        image,
        (new_width, new_height)
    )

    eat_frames.append(image)
# ============================================================
# OBJECT IMAGES
# ============================================================

water_width = 40
water_height = 65

water_image = load_image(
    "assets/water_bottle.png",
    (water_width, water_height)
)

junk_width = 90
junk_height = 60

junk_image = load_image(
    "assets/junk_food.png",
    (junk_width, junk_height)
)

book_width = 75
book_height = 65

book_image = load_image(
    "assets/book.png",
    (book_width, book_height)
)

dumbbell_width = 85
dumbbell_height = 55

dumbbell_image = load_image(
    "assets/dumbbell.png",
    (dumbbell_width, dumbbell_height)
)

mirror_width = 115
mirror_height = 170

mirror_image = load_image(
    "assets/photo_mirror.png",
    (mirror_width, mirror_height)
)

# ============================================================
# NEW: HEALTHY MEALS
# ============================================================

meal_width = 64
meal_height = 52

meal_images = {
    "breakfast": load_image(
        "assets/breakfast_bowl.png",
        (meal_width, meal_height)
    ),
    "lunch": load_image(
        "assets/lunch_bowl.png",
        (meal_width, meal_height)
    ),
    "dinner": load_image(
        "assets/dinner_bowl.png",
        (meal_width, meal_height)
    ),
}

# ============================================================
# SOUNDS
# ============================================================

water_ding = load_sound("assets/water_ding.wav")
junk_food_sound = load_sound("assets/junk_food_hit.wav")
book_read_sound = load_sound("assets/book_read.wav")

# ============================================================
# PLAYER SETTINGS
# ============================================================

lav_x = 100
lav_y = GROUND_Y

lav_speed = 5
lav_y_velocity = 0

gravity = 1
jump_strength = -16

run_animation_index = 0.0
run_animation_speed = 0.15

jump_animation_index = 0.0
jump_animation_speed = 0.12

camera_x = 0

# ============================================================
# WATER CHALLENGE
# ============================================================

water_bottles = [
    {"x": 650, "y": 385, "collected": False},
    {"x": 1200, "y": 385, "collected": False},
    {"x": 1600, "y": 385, "collected": False},
    {"x": 2050, "y": 385, "collected": False},
    {"x": 2550, "y": 385, "collected": False},
]

water_count = 0
water_goal = 5

drinking_active = False
drink_animation_index = 0.0
drink_animation_speed = 0.10

current_water_bottle = None

# ============================================================
# JUNK FOOD
# ============================================================

junk_x = 900
junk_y = 390

junk_collision_cooldown = 0

# ============================================================
# READING CHALLENGE
# ============================================================

book_x = 1825
book_y = 385

book_read = False
book_interaction_distance = 100

reading_active = False
read_animation_index = 0.0
read_animation_speed = 0.035

# ============================================================
# WORKOUT CHALLENGE
# ============================================================

dumbbell_x = 2250
dumbbell_y = 395

workout_interaction_distance = 110

workout_active = False
workout_complete = False

workout_reps = 0
workout_goal = 10

workout_rep_animating = False
workout_animation_index = 0.0
workout_animation_speed = 0.18

# ============================================================
# PHOTO CHALLENGE
# ============================================================

mirror_x = 2740
mirror_y = 280

photo_interaction_distance = 120

photo_active = False
photo_complete = False

photo_animation_index = 0.0
photo_animation_speed = 0.035

photo_flash_timer = 0
photo_flash_triggered = False

# ============================================================
# NEW: DIET CHALLENGE
# ============================================================

meals = [
    {
        "name": "breakfast",
        "x": 350,
        "y": 397,
        "eaten": False
    },
    {
        "name": "lunch",
        "x": 1450,
        "y": 397,
        "eaten": False
    },
    {
        "name": "dinner",
        "x": 2380,
        "y": 397,
        "eaten": False
    },
]

meal_goal = len(meals)
meal_count = 0

meal_interaction_distance = 85

eating_active = False
eat_animation_index = 0.0
eat_animation_speed = 0.055

current_meal = None

# ============================================================
# FLOATING POPUPS
# ============================================================

popups = []


def add_popup(message, world_x, y, color=WHITE, duration=90):
    popups.append({
        "message": message,
        "world_x": world_x,
        "y": float(y),
        "color": color,
        "timer": duration
    })


def draw_popups(camera_offset):
    for popup in popups[:]:
        text = font.render(
            popup["message"],
            True,
            popup["color"]
        )

        screen_x = (
            popup["world_x"]
            - camera_offset
            - text.get_width() // 2
        )

        screen.blit(
            text,
            (screen_x, int(popup["y"]))
        )

        popup["y"] -= 0.5
        popup["timer"] -= 1

        if popup["timer"] <= 0:
            popups.remove(popup)


# ============================================================
# INTERACTION HELPERS
# ============================================================

def player_center():
    return lav_x + lav_width // 2


def is_near(object_x, object_width, distance):
    object_center = object_x + object_width // 2

    return abs(
        player_center() - object_center
    ) <= distance


def draw_prompt(message, world_x, y):
    text = small_font.render(
        message,
        True,
        WHITE
    )

    screen_x = world_x - camera_x

    screen.blit(
        text,
        (
            screen_x - text.get_width() // 2,
            y
        )
    )


# ============================================================
# MAIN GAME LOOP
# ============================================================

running = True

while running:

    # --------------------------------------------------------
    # ACTIVE ANIMATIONS
    # --------------------------------------------------------

    busy = (
        drinking_active
        or reading_active
        or workout_active
        or photo_active
        or eating_active
    )

    # --------------------------------------------------------
    # EVENTS
    # --------------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # ------------------------------------------------
            # E = EAT HEALTHY MEAL
            # ------------------------------------------------

            if (
                event.key == pygame.K_e
                and not busy
                and lav_y == GROUND_Y
            ):

                for meal in meals:

                    if meal["eaten"]:
                        continue

                    if is_near(
                        meal["x"],
                        meal_width,
                        meal_interaction_distance
                    ):

                        eating_active = True
                        current_meal = meal

                        eat_animation_index = 0.0
                        lav_y_velocity = 0

                        print(
                            f"Eating {meal['name']}!"
                        )

                        break

            # ------------------------------------------------
            # R = READ
            # ------------------------------------------------

            elif (
                event.key == pygame.K_r
                and not busy
                and not book_read
                and lav_y == GROUND_Y
            ):

                if is_near(
                    book_x,
                    book_width,
                    book_interaction_distance
                ):

                    reading_active = True
                    read_animation_index = 0.0

                    lav_y_velocity = 0

                    play_sound(book_read_sound)

                    print("Reading started!")

            # ------------------------------------------------
            # P = TAKE PROGRESS PHOTO
            # ------------------------------------------------

            elif (
                event.key == pygame.K_p
                and not busy
                and not photo_complete
                and lav_y == GROUND_Y
            ):

                if is_near(
                    mirror_x,
                    mirror_width,
                    photo_interaction_distance
                ):

                    photo_active = True

                    photo_animation_index = 0.0
                    photo_flash_triggered = False

                    lav_y_velocity = 0

                    print("Progress photo started!")

            # ------------------------------------------------
            # W = START WORKOUT
            # ------------------------------------------------

            elif (
                event.key == pygame.K_w
                and not busy
                and not workout_complete
                and lav_y == GROUND_Y
            ):

                if is_near(
                    dumbbell_x,
                    dumbbell_width,
                    workout_interaction_distance
                ):

                    workout_active = True
                    workout_reps = 0

                    workout_rep_animating = False
                    workout_animation_index = 0.0

                    print("Workout started!")

            # ------------------------------------------------
            # SPACE = ONE WORKOUT REP
            # ------------------------------------------------

            elif (
                event.key == pygame.K_SPACE
                and workout_active
                and not workout_rep_animating
            ):

                workout_rep_animating = True
                workout_animation_index = 0.0

    # --------------------------------------------------------
    # KEYBOARD
    # --------------------------------------------------------

    keys = pygame.key.get_pressed()

    busy = (
        drinking_active
        or reading_active
        or workout_active
        or photo_active
        or eating_active
    )

    # --------------------------------------------------------
    # MOVEMENT
    # --------------------------------------------------------

    if not busy:

        if keys[pygame.K_LEFT]:
            lav_x -= lav_speed

        if keys[pygame.K_RIGHT]:
            lav_x += lav_speed

        lav_x = max(
            0,
            min(lav_x, WORLD_WIDTH - lav_width)
        )

    # --------------------------------------------------------
    # RUNNING ANIMATION
    # --------------------------------------------------------

    moving = (
        keys[pygame.K_LEFT]
        or keys[pygame.K_RIGHT]
    )

    if moving and lav_y == GROUND_Y and not busy:

        run_animation_index += run_animation_speed

        if run_animation_index >= len(run_frames):
            run_animation_index = 0.0

    else:
        run_animation_index = 0.0

    # --------------------------------------------------------
    # JUMP
    # --------------------------------------------------------

    if (
        keys[pygame.K_SPACE]
        and lav_y == GROUND_Y
        and not busy
    ):
        lav_y_velocity = jump_strength

    # --------------------------------------------------------
    # GRAVITY
    # --------------------------------------------------------

    lav_y_velocity += gravity
    lav_y += lav_y_velocity

    if lav_y >= GROUND_Y:
        lav_y = GROUND_Y
        lav_y_velocity = 0

    # --------------------------------------------------------
    # JUMP ANIMATION
    # --------------------------------------------------------

    if lav_y < GROUND_Y and not busy:

        jump_animation_index += jump_animation_speed

        if jump_animation_index >= len(jump_frames):
            jump_animation_index = len(jump_frames) - 1

    else:
        jump_animation_index = 0.0

    # ========================================================
    # NEW: EATING ANIMATION
    # ========================================================

    if eating_active:

        eat_animation_index += eat_animation_speed

        if eat_animation_index >= len(eat_frames):

            eating_active = False
            eat_animation_index = 0.0

            if current_meal is not None:

                current_meal["eaten"] = True

                meal_count += 1

                print(
                    f"Meal {meal_count}/{meal_goal}"
                )

                if meal_count >= meal_goal:

                    add_popup(
                        "DIET COMPLETE!",
                        player_center(),
                        lav_y - 10
                    )

                    print("Diet challenge complete!")

                else:

                    add_popup(
                        "+1 MEAL!",
                        player_center(),
                        lav_y - 10
                    )

                current_meal = None

    # ========================================================
    # WORKOUT ANIMATION
    # ========================================================

    if workout_active and workout_rep_animating:

        workout_animation_index += workout_animation_speed

        if workout_animation_index >= len(workout_frames):

            workout_rep_animating = False
            workout_animation_index = 0.0

            workout_reps += 1

            print(
                f"Rep {workout_reps}/{workout_goal}"
            )

            if workout_reps >= workout_goal:

                workout_reps = workout_goal
                workout_active = False
                workout_complete = True

                add_popup(
                    "WORKOUT COMPLETE!",
                    player_center(),
                    lav_y - 10
                )

                print("Workout complete!")

    # ========================================================
    # DRINKING ANIMATION
    # ========================================================

    if drinking_active:

        drink_animation_index += drink_animation_speed

        if drink_animation_index >= len(drink_frames):

            drinking_active = False
            drink_animation_index = 0.0

            if current_water_bottle is not None:

                current_water_bottle["collected"] = True

                water_count += 1

                add_popup(
                    "+1 WATER!",
                    player_center(),
                    lav_y - 10,
                    duration=60
                )

                play_sound(water_ding)

                print(
                    f"Water {water_count}/{water_goal}"
                )

                current_water_bottle = None

    # ========================================================
    # READING ANIMATION
    # ========================================================

    if reading_active:

        read_animation_index += read_animation_speed

        if read_animation_index >= len(read_frames):

            reading_active = False
            read_animation_index = 0.0

            book_read = True

            add_popup(
                "10 PAGES COMPLETE!",
                player_center(),
                lav_y - 10
            )

            print("10 pages complete!")

    # ========================================================
    # PHOTO ANIMATION
    # ========================================================

    if photo_active:

        photo_animation_index += photo_animation_speed

        if (
            photo_animation_index >= 2.0
            and not photo_flash_triggered
        ):

            photo_flash_timer = 10
            photo_flash_triggered = True

        if photo_animation_index >= len(photo_frames):

            photo_active = False
            photo_animation_index = 0.0

            photo_complete = True

            add_popup(
                "PROGRESS PHOTO COMPLETE!",
                player_center(),
                lav_y - 10
            )

            print("Progress photo complete!")

    # ========================================================
    # CAMERA
    # ========================================================

    camera_x = lav_x - WIDTH // 2

    camera_x = max(
        0,
        min(camera_x, WORLD_WIDTH - WIDTH)
    )

    # ========================================================
    # COLLISION RECTANGLES
    # ========================================================

    lav_rect = pygame.Rect(
        int(lav_x + 15),
        int(lav_y + 20),
        40,
        75
    )

    junk_rect = pygame.Rect(
        junk_x + 20,
        junk_y + 25,
        50,
        30
    )

    # ========================================================
    # WATER COLLISION
    # ========================================================

    busy = (
        drinking_active
        or reading_active
        or workout_active
        or photo_active
        or eating_active
    )

    if not busy:

        for bottle in water_bottles:

            if bottle["collected"]:
                continue

            bottle_rect = pygame.Rect(
                bottle["x"],
                bottle["y"],
                water_width,
                water_height
            )

            if lav_rect.colliderect(bottle_rect):

                drinking_active = True

                drink_animation_index = 0.0

                current_water_bottle = bottle

                lav_y_velocity = 0

                break

    # ========================================================
    # JUNK FOOD COLLISION
    # ========================================================

    if junk_collision_cooldown > 0:
        junk_collision_cooldown -= 1

    busy = (
        drinking_active
        or reading_active
        or workout_active
        or photo_active
        or eating_active
    )

    if (
        lav_rect.colliderect(junk_rect)
        and junk_collision_cooldown == 0
        and not busy
    ):

        play_sound(junk_food_sound)

        add_popup(
            "! JUNK FOOD !",
            player_center(),
            lav_y - 10,
            RED,
            60
        )

        lav_x = max(0, lav_x - 80)

        junk_collision_cooldown = 30

        print("Oops! Junk food!")

    # ========================================================
    # NEARBY INTERACTIONS
    # ========================================================

    busy = (
        drinking_active
        or reading_active
        or workout_active
        or photo_active
        or eating_active
    )

    near_book = (
        not busy
        and not book_read
        and is_near(
            book_x,
            book_width,
            book_interaction_distance
        )
    )

    near_dumbbell = (
        not busy
        and not workout_complete
        and is_near(
            dumbbell_x,
            dumbbell_width,
            workout_interaction_distance
        )
    )

    near_mirror = (
        not busy
        and not photo_complete
        and is_near(
            mirror_x,
            mirror_width,
            photo_interaction_distance
        )
    )

    # NEW: Find nearby uneaten meal
    near_meal = None

    if not busy:

        for meal in meals:

            if meal["eaten"]:
                continue

            if is_near(
                meal["x"],
                meal_width,
                meal_interaction_distance
            ):

                near_meal = meal
                break

    # ========================================================
    # DRAW BACKGROUND
    # ========================================================

    background_offset = camera_x % WIDTH

    screen.blit(
        background_image,
        (-background_offset, 0)
    )

    screen.blit(
        background_image,
        (WIDTH - background_offset, 0)
    )

    # ========================================================
    # DRAW WATER
    # ========================================================

    for bottle in water_bottles:

        if not bottle["collected"]:

            screen.blit(
                water_image,
                (
                    bottle["x"] - camera_x,
                    bottle["y"]
                )
            )

    # ========================================================
    # DRAW JUNK FOOD
    # ========================================================

    screen.blit(
        junk_image,
        (junk_x - camera_x, junk_y)
    )

    # ========================================================
    # DRAW BOOK
    # ========================================================

    if not book_read and not reading_active:

        screen.blit(
            book_image,
            (book_x - camera_x, book_y)
        )

    # ========================================================
    # DRAW DUMBBELL
    # ========================================================

    if not workout_complete:

        screen.blit(
            dumbbell_image,
            (dumbbell_x - camera_x, dumbbell_y)
        )

    # ========================================================
    # DRAW PHOTO MIRROR
    # ========================================================

    screen.blit(
        mirror_image,
        (mirror_x - camera_x, mirror_y)
    )

    # ========================================================
    # NEW: DRAW HEALTHY MEALS
    # ========================================================

    for meal in meals:

        if not meal["eaten"]:

            meal_image = meal_images[meal["name"]]

            screen.blit(
                meal_image,
                (
                    meal["x"] - camera_x,
                    meal["y"]
                )
            )

    # ========================================================
    # DRAW LAV
    # ========================================================

    lav_screen_x = lav_x - camera_x

    if eating_active:

        frame_number = min(
            int(eat_animation_index),
            len(eat_frames) - 1
        )

        current_frame = eat_frames[frame_number]

    elif photo_active:

        frame_number = min(
            int(photo_animation_index),
            len(photo_frames) - 1
        )

        current_frame = photo_frames[frame_number]

    elif reading_active:

        frame_number = min(
            int(read_animation_index),
            len(read_frames) - 1
        )

        current_frame = read_frames[frame_number]

    elif drinking_active:

        frame_number = min(
            int(drink_animation_index),
            len(drink_frames) - 1
        )

        current_frame = drink_frames[frame_number]

    elif workout_active:

        if workout_rep_animating:

            frame_number = min(
                int(workout_animation_index),
                len(workout_frames) - 1
            )

            current_frame = workout_frames[frame_number]

        else:
            current_frame = workout_frames[0]

    elif lav_y < GROUND_Y:

        current_frame = jump_frames[
            int(jump_animation_index)
        ]

    elif keys[pygame.K_RIGHT]:

        current_frame = run_frames[
            int(run_animation_index)
        ]

    elif keys[pygame.K_LEFT]:

        current_frame = pygame.transform.flip(
            run_frames[int(run_animation_index)],
            True,
            False
        )

    else:

        current_frame = lav_image

    screen.blit(
        current_frame,
        (lav_screen_x, lav_y)
    )

    # ========================================================
    # NEW: PRESS E TO EAT
    # ========================================================

    if near_meal is not None:

        draw_prompt(
            "Press E to Eat",
            near_meal["x"] + meal_width // 2,
            near_meal["y"] - 34
        )

    # ========================================================
    # PRESS R TO READ
    # ========================================================

    if near_book:

        draw_prompt(
            "Press R to Read",
            book_x + book_width // 2,
            book_y - 35
        )

    # ========================================================
    # PRESS W TO WORKOUT
    # ========================================================

    if near_dumbbell:

        draw_prompt(
            "Press W to Workout",
            dumbbell_x + dumbbell_width // 2,
            dumbbell_y - 35
        )

    # ========================================================
    # PRESS P TO TAKE PHOTO
    # ========================================================

    if near_mirror:

        draw_prompt(
            "Press P to Take Photo",
            mirror_x + mirror_width // 2,
            mirror_y - 30
        )

    # ========================================================
    # WORKOUT MODE
    # ========================================================

    if workout_active:

        draw_centered(
            "WORKOUT",
            65
        )

        draw_centered(
            f"{workout_reps}/{workout_goal} REPS",
            100
        )

        if workout_rep_animating:
            workout_prompt = "CURL..."
        else:
            workout_prompt = "SPACE = 1 REP"

        draw_centered(
            workout_prompt,
            135,
            small_font
        )

    # ========================================================
    # FLOATING POPUPS
    # ========================================================

    draw_popups(camera_x)

    # ========================================================
    # CAMERA FLASH
    # ========================================================

    if photo_flash_timer > 0:

        flash_surface = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        flash_surface.fill(
            (
                255,
                255,
                255,
                min(220, photo_flash_timer * 22)
            )
        )

        screen.blit(
            flash_surface,
            (0, 0)
        )

        photo_flash_timer -= 1

    # ========================================================
    # 75 HARD HUD
    # ========================================================

    hud_x = 15
    hud_y = 15

    hud_width = 210
    hud_height = 205

    hud_surface = pygame.Surface(
        (hud_width, hud_height),
        pygame.SRCALPHA
    )

    hud_surface.fill(
        (255, 220, 235, 210)
    )

    screen.blit(
        hud_surface,
        (hud_x, hud_y)
    )

    hud_title = hud_title_font.render(
        "75 HARD - DAY 1",
        True,
        DARK_PINK
    )

    screen.blit(
        hud_title,
        (hud_x + 15, hud_y + 12)
    )

    # --------------------------------------------------------
    # HUD STATUSES
    # --------------------------------------------------------

    water_status = f"{water_count}/{water_goal}"

    read_status = (
        "DONE" if book_read else "--"
    )

    if workout_complete:
        workout_status = "DONE"

    elif workout_active:
        workout_status = f"{workout_reps}/{workout_goal}"

    else:
        workout_status = "--"

    photo_status = (
        "DONE" if photo_complete else "--"
    )

    # NEW: DIET PROGRESS
    if meal_count >= meal_goal:
        diet_status = "DONE"
    else:
        diet_status = f"{meal_count}/{meal_goal}"

    tasks = [
        ("WATER", water_status),
        ("READ", read_status),
        ("WORKOUT", workout_status),
        ("OUTDOOR", "--"),
        ("DIET", diet_status),
        ("PHOTO", photo_status),
    ]

    task_y = hud_y + 50

    for task_name, task_status in tasks:

        task_text = hud_font.render(
            task_name,
            True,
            DARK_PINK
        )

        screen.blit(
            task_text,
            (hud_x + 15, task_y)
        )

        status_text = hud_font.render(
            task_status,
            True,
            WHITE
        )

        status_x = (
            hud_x
            + hud_width
            - status_text.get_width()
            - 15
        )

        screen.blit(
            status_text,
            (status_x, task_y)
        )

        task_y += 24

    # ========================================================
    # UPDATE SCREEN
    # ========================================================

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()