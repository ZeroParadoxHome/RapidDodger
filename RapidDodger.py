import pygame
import random
import time
import os


# Function to clear the console screen.
def clear_console():
    command = "cls" if os.name == "nt" else "clear"
    return os.system(command)


# Function to display a welcome message to the user.
def display_welcome_message():
    print(
        "\033[92mWelcome to the \033[0m\033[97mZeroParadox Code\033[0m\033[92m.\n\n\033[92mPlease run this code with \033[0m\033[91mPython 3\033[0m\033[92m!\033[0m"
    )


# Function to initialize the game and return game-related variables.
def initialize_game():
    global Custom_Red, Custom_Green, Custom_Blue, Black, White, Red, Dark_Red, Light_Red, Green, Dark_Green, Light_Green, Blue, Dark_Blue, Light_Blue, Lime, Yellow, Silver, car_img, intro_page
    Black = (0, 0, 0)
    White = (255, 255, 255)
    Red = (255, 0, 0)
    Dark_Red = (139, 0, 0)
    Light_Red = (255, 99, 71)
    Custom_Red = (255, 64, 64)
    Green = (0, 128, 0)
    Dark_Green = (0, 100, 0)
    Light_Green = (144, 238, 144)
    Custom_Green = (0, 255, 128)
    Blue = (0, 0, 255)
    Dark_Blue = (0, 0, 139)
    Light_Blue = (173, 216, 230)
    Custom_Blue = (102, 178, 255)
    Lime = (0, 255, 0)
    Yellow = (255, 255, 0)
    Silver = (192, 192, 192)
    pygame.init()
    pygame.mixer.music.load("Audios/Trance.mp3")
    crash_sound = pygame.mixer.Sound("Audios/Lose.wav")
    monitor_info = pygame.display.Info()
    display_width = int(monitor_info.current_w * 0.6)
    display_height = int(monitor_info.current_h * 0.8)
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    game_display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("RapidDodger: The Zero Paradox Challenge!")
    car_img = pygame.image.load("vehicle_assets/1.png")
    car_rect = car_img.get_rect()
    car_width = car_rect.width
    car_height = car_rect.height
    clock = pygame.time.Clock()
    intro_page = True
    return (
        crash_sound,
        display_width,
        display_height,
        game_display,
        clock,
        car_img,
        car_width,
        car_height,
        intro_page,
    )


# Function to draw a button on the game screen.
def draw_button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_rect = pygame.Rect(x, y, w, h)
    if button_rect.collidepoint(mouse):
        pygame.draw.rect(game_display, ac, button_rect)
        if click[0] == 1 and action is not None:
            if action == "Play":
                game_loop()
            elif action == "Exit":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(game_display, ic, button_rect)

    font = pygame.font.Font("Vazirmatn-SemiBold.ttf", 20)
    text_surf = font.render(msg, True, Black)
    text_rect = text_surf.get_rect(center=button_rect.center)
    game_display.blit(text_surf, text_rect)


# Function to draw obstacles on the game screen.
def draw_obstacle(x, y, width, height, shape_type, color):
    if shape_type == "square":
        pygame.draw.rect(game_display, color, [x, y, width, height])
    elif shape_type == "rectangle":
        pygame.draw.rect(game_display, color, [x, y, width * 2, height])
    elif shape_type == "circle":
        pygame.draw.circle(
            game_display, color, (x + width // 2, y + height // 2), width // 2
        )


# Function to draw the car on the game screen.
def draw_car(x, y):
    game_display.blit(car_img, (x, y))


# Function to set the car icon based on the selected index.
def set_car_icon(icon_index):
    global car_img
    car_img = pygame.image.load(f"vehicle_assets/{icon_index}.png")


# Function to create text objects.
def text_objects(text, font):
    text_surface = font.render(text, True, Black)
    return text_surface, text_surface.get_rect()


# Function to display a message on the game screen.
def display_message(text, color, position, size):
    font = pygame.font.Font("Vazirmatn-SemiBold.ttf", size)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=position)
    game_display.blit(text_surf, text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)


# Function to display the introduction screen of the game.
def display_intro():
    play_button = pygame.Rect(150, 450, 100, 50)
    exit_button = pygame.Rect(550, 450, 100, 50)
    settings_icon = pygame.image.load("Icons/settings.png")
    help_icon = pygame.image.load("Icons/info.png")
    display_center_x = display_width / 2
    display_center_y = display_height / 2
    settings_icon_x = display_width - settings_icon.get_width() + 20
    settings_icon_y = display_height - settings_icon.get_height() - 20
    help_icon_x = 20
    help_icon_y = display_height - help_icon.get_height() - 20
    settings_icon_rect = settings_icon.get_rect(
        bottomright=(settings_icon_x, settings_icon_y)
    )
    help_icon_rect = help_icon.get_rect(bottomleft=(help_icon_x, help_icon_y))
    credits_button_width = 100
    credits_button_height = 50
    center_x = display_width // 2
    bottom_y = display_height - 50
    button_x = center_x - credits_button_width // 2
    button_y = bottom_y - credits_button_height
    credits_button = pygame.Rect(
        button_x, button_y, credits_button_width, credits_button_height
    )
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if settings_icon_rect.collidepoint(event.pos):
                    display_settings()
                if help_icon_rect.collidepoint(event.pos):
                    display_instructions()
                if credits_button.collidepoint(event.pos):
                    display_credits()
        game_display.fill(Custom_Blue)
        title_text = pygame.font.Font("Vazirmatn-SemiBold.ttf", 120)
        text_surf, text_rect = text_objects("Let's Play", title_text)
        text_rect.center = (display_center_x, display_center_y)
        game_display.blit(text_surf, text_rect)
        game_display.blit(settings_icon, settings_icon_rect)
        game_display.blit(help_icon, help_icon_rect)
        play_button.center = (display_center_x - 100, display_center_y + 200)
        exit_button.center = (display_center_x + 100, display_center_y + 200)
        pygame.draw.rect(game_display, Green, play_button)
        pygame.draw.rect(game_display, Red, exit_button)
        draw_button(
            "Play", *play_button.topleft, *play_button.size, Green, Custom_Green, "Play"
        )
        draw_button(
            "Exit", *exit_button.topleft, *exit_button.size, Red, Custom_Red, "Exit"
        )
        draw_button(
            "Credits",
            *credits_button.topleft,
            *credits_button.size,
            (0, 0, 204),
            (0, 102, 204),
        )
        pygame.display.flip()


# Function to display the settings menu.
def display_settings():
    global intro_page
    settings_page = True
    while settings_page:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if settings_rect.collidepoint(event.pos):
                        for icon_rect in icon_rects:
                            if icon_rect.collidepoint(event.pos):
                                set_car_icon(icon_rects.index(icon_rect) + 1)
                                display_message(
                                    "OK, Icon Selected. Enjoy the game!",
                                    Red,
                                    (display_width // 2, display_height // 4),
                                    55,
                                )
                                display_intro()
                    else:
                        if back_button_rect.collidepoint(event.pos):
                            display_intro()
        game_display.fill(White)
        settings_rect = pygame.Rect(100, 100, display_width - 200, display_height - 200)
        pygame.draw.rect(game_display, Black, settings_rect, 2)
        icon_folder = "vehicle_assets"
        icons_per_row = 7
        icon_size = 50
        icon_spacing = 52
        icon_images = []
        for i in range(1, 15):
            icon_images.append(pygame.image.load(f"{icon_folder}/{i}.png"))
        total_icons = len(icon_images)
        rows = total_icons // icons_per_row + (1 if total_icons % icons_per_row else 0)
        total_width_needed = (
            icons_per_row * icon_size + (icons_per_row - 1) * icon_spacing
        )
        margin_x = (display_width - total_width_needed) / 2
        margin_y = (display_height - rows * icon_size - (rows - 1) * icon_spacing) / 2
        for i, icon in enumerate(icon_images):
            row = i // icons_per_row
            col = i % icons_per_row
            x = margin_x + col * (icon_size + icon_spacing)
            y = margin_y + row * (icon_size + icon_spacing)
            game_display.blit(icon, (x, y))
        back_icon = pygame.image.load("Icons/back.png")
        back_button_rect = back_icon.get_rect()
        back_button_rect.bottomleft = (20, display_height - 20)
        game_display.blit(back_icon, back_button_rect)
        icon_rects = []
        for i, icon in enumerate(icon_images):
            row = i // icons_per_row
            col = i % icons_per_row
            x = margin_x + col * (icon_size + icon_spacing)
            y = margin_y + row * (icon_size + icon_spacing)
            icon_rect = pygame.Rect(x, y, icon_size, icon_size)
            icon_rects.append(icon_rect)
            game_display.blit(icon, (x, y))
        pygame.display.flip()


# Function to display the instructions screen.
def display_instructions():
    instructions_page = True
    while instructions_page:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_button_rect.collidepoint(event.pos):
                        display_intro()

        game_display.fill(White)

        text = r"Coming Soon!, Not supported yet."
        font = pygame.font.Font("Vazirmatn-SemiBold.ttf", 36)
        font.set_underline(True)
        text_render = font.render(text, True, Black)
        text_rect = text_render.get_rect(
            center=(display_width // 2, display_height // 2)
        )
        game_display.blit(text_render, text_rect)
        back_icon = pygame.image.load("Icons/back.png")
        back_button_rect = back_icon.get_rect(bottomleft=(20, display_height - 20))
        game_display.blit(back_icon, back_button_rect)
        pygame.display.flip()
        clock.tick(35)


# Function to display the about page.
def display_credits():
    credits = True
    while credits:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    display_intro()
        game_display.fill(White)
        font = pygame.font.Font("Vazirmatn-SemiBold.ttf", 28)
        text = r"Rapid Dodger is developed by [ ZeroParadoxHome ] using Python and Pygame library."
        text_render = font.render(text, True, Black)
        text_rect = text_render.get_rect(
            center=(display_width // 2, display_height // 2)
        )
        game_display.blit(text_render, text_rect)
        back_icon = pygame.image.load("Icons/back.png")
        back_button_rect = back_icon.get_rect(bottomleft=(20, display_height - 20))
        game_display.blit(back_icon, back_button_rect)
        pygame.display.flip()
        clock.tick(35)


# Function to display the current score, total score, and time on the game screen.
def display_score(count, total_score, minutes, seconds, highest_score):
    font = pygame.font.Font("Vazirmatn-SemiBold.ttf", 18)
    score_text = (
        f"Score: {count} | Total Score: {total_score} | Highest Score: {highest_score}"
    )
    time_text = f"Time: {minutes:02d}:{seconds:02d}"
    score_surface = font.render(score_text, True, Black)
    time_surface = font.render(time_text, True, Black)
    game_display.blit(score_surface, (1, 1))
    game_display.blit(time_surface, (1, 30))


# Function to read the high score from a file.
def read_highest_score():
    try:
        with open("highest_score.txt", "r") as file:
            highest_score = int(file.read())
    except FileNotFoundError:
        highest_score = 0
    return highest_score


# Function to write the high score to a file.
def write_highest_score(score):
    with open("highest_score.txt", "w") as file:
        file.write(str(score))


# Function to check for collisions between the car and obstacles.
def is_collision(
    car_x,
    car_y,
    car_width,
    car_height,
    obstacle_x,
    obstacle_y,
    obstacle_width,
    obstacle_height,
    shape_type,
):
    if shape_type == "rectangle":
        if car_y < obstacle_y + obstacle_height and car_y + car_height > obstacle_y:
            if (
                car_x + car_width > obstacle_x
                and car_x < obstacle_x + obstacle_width * 2
            ):
                return True
    else:
        if car_y < obstacle_y + obstacle_height and car_y + car_height > obstacle_y:
            if car_x + car_width > obstacle_x and car_x < obstacle_x + obstacle_width:
                return True
    return False


# Function to handle the game crash event.
def handle_crash():
    global display_width, display_height
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)
    title_text = pygame.font.Font("Vazirmatn-SemiBold.ttf", 120)
    text_surf, text_rect = text_objects("Game Over", title_text)
    crash_loop = True
    while crash_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        text_rect.center = (display_width / 2, display_height / 2)
        game_display.blit(text_surf, text_rect)
        button_center_x = display_width / 2
        button_center_y = display_height / 2 + 150
        draw_button(
            "Play More",
            button_center_x - 215,
            button_center_y,
            100,
            50,
            Green,
            Custom_Green,
            "Play",
        )
        draw_button(
            "Exit",
            button_center_x + 125,
            button_center_y,
            100,
            50,
            Red,
            Custom_Red,
            "Exit",
        )
        pygame.display.flip()


# Main game function.
def game_loop():
    shapes = ["square", "rectangle", "circle"]
    color_list = [
        Black,
        White,
        Red,
        Dark_Red,
        Light_Red,
        Green,
        Dark_Green,
        Light_Green,
        Blue,
        Dark_Blue,
        Light_Blue,
        Lime,
        Yellow,
        Silver,
    ]
    shape_colors = {
        "square": random.choice(color_list),
        "rectangle": random.choice(color_list),
        "circle": random.choice(color_list),
    }
    pygame.mixer.music.play(-1)
    start_time = time.time()
    x = display_width * 0.45
    y = display_height * 0.8
    obstacle_start_x = random.randrange(0, display_width)
    highest_score = read_highest_score()
    current_shape_index = 0
    obstacle_start_y = -700
    obstacle_width = 75
    obstacle_height = 75
    obstacle_speed = 7
    dodged = 0
    x_change = 0
    GameExit = False
    while not GameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -6
                elif event.key == pygame.K_RIGHT:
                    x_change = 6
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        x += x_change
        game_display.fill(Custom_Blue)
        shape_type = shapes[current_shape_index]
        color = shape_colors[shape_type]
        draw_obstacle(
            obstacle_start_x,
            obstacle_start_y,
            obstacle_width,
            obstacle_height,
            shape_type,
            color,
        )
        obstacle_start_y += obstacle_speed
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_score = int(elapsed_time)
        dodged_score = dodged
        total_score = time_score + dodged_score
        display_score(dodged, total_score, minutes, seconds, highest_score)
        draw_car(x, y)
        if x > display_width - car_width or x < 0:
            handle_crash()
        if is_collision(
            x,
            y,
            car_width,
            car_height,
            obstacle_start_x,
            obstacle_start_y,
            obstacle_width,
            obstacle_height,
            shape_type,
        ):
            handle_crash()
        if obstacle_start_y > display_height:
            obstacle_start_x = random.randrange(0, display_width)
            obstacle_start_y = 0 - obstacle_height
            dodged += 1
            current_shape_index += 1
            if current_shape_index == len(shapes):
                current_shape_index = 0
            if dodged % 5 == 0:
                obstacle_speed += elapsed_time * 0.01
                obstacle_width += 5
                obstacle_height += 5
                shape_colors = {
                    "square": random.choice(color_list),
                    "rectangle": random.choice(color_list),
                    "circle": random.choice(color_list),
                }
        pygame.display.flip()
        clock.tick(110)
        if total_score > highest_score:
            highest_score = total_score
            write_highest_score(highest_score)


clear_console()
display_welcome_message()
(
    crash_sound,
    display_width,
    display_height,
    game_display,
    clock,
    car_img,
    car_width,
    car_height,
    intro_page,
) = initialize_game()
display_intro()
game_loop()
pygame.quit()
quit()
