# FULLY FIXED brick_breaker_game.py WITH AUDIO SLIDER WORKING
import pygame
import sys

# ============ INIT ============
import json
import os

def load_settings():
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as f:
            return json.load(f)
    return {"resolution": "800x600", "fullscreen": False, "vsync": False}

def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f)

settings = load_settings()
WIDTH, HEIGHT = map(int, settings["resolution"].split("x"))
fullscreen = settings.get("fullscreen", False)
vsync = settings.get("vsync", False)
import cv2
import random  # make sure this is near the top if not already there

video_files = ["mainmenuvideo.mp4", "mainmenuvideo2.mp4"]
selected_video = random.choice(video_files)
print(f"Selected main menu video: {selected_video}")

video = cv2.VideoCapture(selected_video)
if not video.isOpened():
    print(f"Failed to open video: {selected_video}")
else:
    video.set(cv2.CAP_PROP_POS_FRAMES, 0)

pygame.init()
motion_blur_enabled = True

# ============ CONFIG ==========
# WIDTH, HEIGHT = 1600, 900  # Removed to preserve settings loading
SCALE_X = WIDTH / 800
SCALE_Y = HEIGHT / 600
flags = pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags | (pygame.FULLSCREEN if fullscreen else 0))
pygame.display.set_caption("Brick Breaker")
clock = pygame.time.Clock()
FPS = 100

# ============ COLORS ============
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# ============ FONTS ============
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

# ============ BACKGROUND ============
background_img = pygame.image.load("image.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# ============ LIVES ============
LIVES = 3

# ============ CLASSES ============
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        width = int(100 * SCALE_X)
        height = int(20 * SCALE_Y)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 200, 255), (0, 0, width, height), border_radius=12)
        pygame.draw.rect(self.image, (255, 105, 180), (4, 4, width - 8, height - 8), border_radius=8)
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - int(50 * SCALE_Y)))

    def mouse_move(self, x):
        target_x = max(self.rect.width // 2, min(WIDTH - self.rect.width // 2, x))
        self.rect.centerx += (target_x - self.rect.centerx) * 0.2

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = int(15 * SCALE_X)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect()
        self.dx = int(4 * SCALE_X)
        self.dy = int(-4 * SCALE_Y)
        self.active = False

    def reset_on_paddle(self, paddle):
        self.rect.centerx = paddle.rect.centerx
        self.rect.bottom = paddle.rect.top - 2

    def update(self):
        if not self.active:
            return
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dx *= -1
        if self.rect.top <= 0:
            self.dy *= -1

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dx *= -1
        if self.rect.top <= 0:
            self.dy *= -1

# ============ BRICKS ============
def create_bricks(level=1):
    class FadingBrick(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h, color):
            super().__init__()
            self.original_image = pygame.Surface((w, h))
            self.original_image.fill(color)
            self.image = self.original_image.copy()
            self.rect = self.image.get_rect(topleft=(x, y))
            self.alpha = 0

        def update(self):
            if self.alpha < 255:
                self.alpha = min(255, self.alpha + 5)
                self.image = self.original_image.copy()
                self.image.set_alpha(self.alpha)
    bricks = pygame.sprite.Group()
    colors = [RED, ORANGE, GREEN, CYAN, BLUE]
    brick_width = int(10 * SCALE_X)
    brick_height = int(8 * SCALE_Y)
    padding = 2

    if level == 1:
        pattern = [
            "00000000000000000000000000000000000000000000000000000000000000000000000000000000",
            "00000000000000000000000000000000000000000000000000000000000000000000000000000000",
            "00000000000000000000000001111111111100000000000000011111111111000000000000000000",
            "00000000000000000000001111111111111111100000000111111111111111110000000000000000",
            "00000000000000000000111111111111111111111000011111111111111111111100000000000000",
            "00000000000000000001111111111111111111111110111111111111111111111110000000000000",
            "00000000000000000011111111111111111111111111111111111111111111111111000000000000",
            "00000000000000000111111111111111111111111111111111111111111111111111100000000000",
            "00000000000000001111111111111111111111111111111111111111111111111111110000000000",
            "00000000000000001111111111111111111111111111111111111111111111111111110000000000",
            "00000000000000011111111111111111111111111111111111111111111111111111111000000000",
            "00000000000000011111111111111111111111111111111111111111111111111111111000000000",
            "00000000000000011111111111111111111111111111111111111111111111111111111000000000",
            "00000000000000001111111111111111111111111111111111111111111111111111110000000000",
            "00000000000000001111111111111111111111111111111111111111111111111111110000000000",
            "00000000000000000111111111111111111111111111111111111111111111111111100000000000",
            "00000000000000000011111111111111111111111111111111111111111111111111000000000000",
            "00000000000000000001111111111111111111111111111111111111111111111110000000000000",
            "00000000000000000000111111111111111111111111111111111111111111111100000000000000",
            "00000000000000000000001111111111111111111111111111111111111111110000000000000000",
            "00000000000000000000000001111111111111111111111111111111111110000000000000000000",
            "00000000000000000000000000000111111111111111111111111111111000000000000000000000",
            "00000000000000000000000000000000011111111111111111111111000000000000000000000000",
            "00000000000000000000000000000000000000111111111111110000000000000000000000000000",
            "00000000000000000000000000000000000000000001111100000000000000000000000000000000",
            "00000000000000000000000000000000000000000000000000000000000000000000000000000000"
        ]
    elif level == 2:
        pattern = [
            "00000",
            "00100",
            "00000"
        ]
    elif level == 3:
        pattern = [
            "000000000000111111111111000000000000",
            "000000001111111111111111111100000000",
            "000001111111111111111111111111000000",
            "000111111100000000000000111111110000",
            "001111110000000000000000001111110000",
            "011111000001111000111100000111111000",
            "011110000011111000111100000011111000",
            "011100000111111000111100000001111000",
            "011100000111111000111100000001111000",
            "011110000011111111111111000011111000",
            "001111000000111111111111000111110000",
            "001111100000001111111100001111100000",
            "000111110000000111111000011111000000",
            "000011111000000000000000111110000000",
            "000001111100000000000001111100000000",
            "000000111111000000000111111000000000",
            "000000011111110000011111110000000000",
            "000000001111111111111111100000000000",
            "000000000111111111111111000000000000",
            "000000000011111111111100000000000000",
            "000000000001111111111000000000000000",
            "000000000000111111110000000000000000",
            "000000000000011111100000000000000000",
            "000000000000001111000000000000000000",
            "000000000000000110000000000000000000"
        ]

    offset_x = WIDTH // 2 - (len(pattern[0]) * (brick_width + padding)) // 2
    offset_y = 60

    for row_idx, row in enumerate(pattern):
        for col_idx, val in enumerate(row):
            if val == "1":
                color = colors[(row_idx + col_idx) % len(colors)]
                x = offset_x + col_idx * (brick_width + padding)
                y = offset_y + row_idx * (brick_height + padding)
                brick = FadingBrick(x, y, brick_width, brick_height, color)
                bricks.add(brick)

    return bricks

# ============ WIN SCREEN ============
def win_screen():
    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)
    background = pygame.image.load("youwin.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    popup_surface = pygame.Surface((int(400 * SCALE_X), int(200 * SCALE_Y)), pygame.SRCALPHA)
    popup_rect = popup_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    restart_btn = pygame.Rect(popup_rect.left + int(50 * SCALE_X), popup_rect.bottom - int(70 * SCALE_Y), int(120 * SCALE_X), int(40 * SCALE_Y))
    quit_btn = pygame.Rect(popup_rect.right - int(170 * SCALE_X), popup_rect.bottom - int(70 * SCALE_Y), int(120 * SCALE_X), int(40 * SCALE_Y))

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL:
                bricks.empty()  # Destroy all bricks instantly

        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.collidepoint(event.pos):
                    return True
                elif quit_btn.collidepoint(event.pos):
                    return False

               
        popup_surface.fill((30, 30, 30, 200))
        screen.blit(popup_surface, popup_rect)

        hover_restart = restart_btn.collidepoint((mx, my))
        hover_quit = quit_btn.collidepoint((mx, my))

        restart_draw = restart_btn.inflate(10, 10) if hover_restart else restart_btn
        quit_draw = quit_btn.inflate(10, 10) if hover_quit else quit_btn

        pygame.draw.rect(screen, GREEN if not hover_restart else (0, 200, 0), restart_draw, border_radius=12)
        pygame.draw.rect(screen, RED if not hover_quit else (200, 0, 0), quit_draw, border_radius=12)

        restart_text = font.render("Restart", True, WHITE)
        screen.blit(restart_text, restart_draw.move((restart_draw.width - restart_text.get_width()) // 2 - 10, 5))
        quit_text = font.render("Quit", True, WHITE)
        screen.blit(quit_text, quit_draw.move((quit_draw.width - quit_text.get_width()) // 2 - 5, 5))

        screen.blit(big_font.render("You Win!", True, CYAN), (WIDTH // 2 - 100, HEIGHT // 2 - 80))

                # Speech bubble for resolution note
        bubble_width = int(480 * SCALE_X)
        bubble_height = int(80 * SCALE_Y)
        bubble_x = int(550 * SCALE_X)
        bubble_y = HEIGHT - bubble_height - 30
        bubble_rect = pygame.Rect(bubble_x, bubble_y, bubble_width, bubble_height)
        pygame.draw.rect(screen, (50, 50, 50), bubble_rect, border_radius=15)
        pygame.draw.polygon(screen, (50, 50, 50), [(bubble_x + bubble_width // 2 - 10, bubble_y + bubble_height), (bubble_x + bubble_width // 2 + 10, bubble_y + bubble_height), (bubble_x + bubble_width // 2, bubble_y + bubble_height + 10)])

        note_text = font.render("keep the resolution in 1600x900 and fullscreen,", True, WHITE)
        note_text2 = font.render("we are working on the scaling (its too hard T-T)", True, WHITE)
        screen.blit(note_text, (bubble_x + 15, bubble_y + 10))
        screen.blit(note_text2, (bubble_x + 15, bubble_y + 40))

                # Draw custom cursor
        screen.blit(custom_cursor, (pygame.mouse.get_pos()[0] + cursor_offset[0], pygame.mouse.get_pos()[1] + cursor_offset[1]))
        pygame.display.flip()
        clock.tick(FPS)


# ============ GAME OVER ============
def game_over_screen():
    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)
    import cv2
    lose_video = None
    try:
        lose_video = cv2.VideoCapture("youlose12.mp4")
        lose_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
    except Exception as e:
        print(f"Lose video load failed: {e}")
    background = pygame.image.load("lost.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    popup_surface = pygame.Surface((int(400 * SCALE_X), int(200 * SCALE_Y)), pygame.SRCALPHA)
    popup_rect = popup_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    restart_btn = pygame.Rect(popup_rect.left + int(50 * SCALE_X), popup_rect.bottom - int(70 * SCALE_Y), int(120 * SCALE_X), int(40 * SCALE_Y))
    quit_btn = pygame.Rect(popup_rect.right - int(170 * SCALE_X), popup_rect.bottom - int(70 * SCALE_Y), int(120 * SCALE_X), int(40 * SCALE_Y))

    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.collidepoint(event.pos):
                    return True
                elif quit_btn.collidepoint(event.pos):
                    return False

        screen.blit(background, (0, 0))
        popup_surface.fill((30, 30, 30, 200))
        screen.blit(popup_surface, popup_rect)

        hover_restart = restart_btn.collidepoint((mx, my))
        hover_quit = quit_btn.collidepoint((mx, my))

        restart_draw = restart_btn.inflate(10, 10) if hover_restart else restart_btn
        quit_draw = quit_btn.inflate(10, 10) if hover_quit else quit_btn

        pygame.draw.rect(screen, GREEN if not hover_restart else (0, 200, 0), restart_draw, border_radius=12)
        pygame.draw.rect(screen, RED if not hover_quit else (200, 0, 0), quit_draw, border_radius=12)

        restart_text = font.render("Restart", True, WHITE)
        screen.blit(restart_text, restart_draw.move((restart_draw.width - restart_text.get_width()) // 2 - 10, 5))
        quit_text = font.render("Quit", True, WHITE)
        screen.blit(quit_text, quit_draw.move((quit_draw.width - quit_text.get_width()) // 2 - 5, 5))

        screen.blit(big_font.render("Game Over", True, CYAN), (WIDTH // 2 - 120, HEIGHT // 2 - 80))

        pygame.display.flip()
        clock.tick(FPS)



        result = True

        
# ============ SETTINGS MENU ============
# ============ SETTINGS STATE ============
RESOLUTIONS = [(800, 600), (1280, 720), (1600, 900), (1920, 1080)]
current_resolution_index = RESOLUTIONS.index((WIDTH, HEIGHT)) if (WIDTH, HEIGHT) in RESOLUTIONS else 0
left_key = pygame.K_LEFT
right_key = pygame.K_RIGHT
rebinding = None
def update_resolution(index, fullscreen_flag):
    global WIDTH, HEIGHT, screen, SCALE_X, SCALE_Y, flags

    settings["resolution"] = f"{RESOLUTIONS[index][0]}x{RESOLUTIONS[index][1]}"
    settings["fullscreen"] = fullscreen_flag
    save_settings(settings)

    WIDTH, HEIGHT = RESOLUTIONS[index]
    SCALE_X = WIDTH / 800
    SCALE_Y = HEIGHT / 600
    flags = pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF
    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT),
        flags | (pygame.FULLSCREEN if fullscreen_flag else 0)
    )

def settings_menu():
    motion_blur = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    background = pygame.image.load("settingbackground.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    global motion_blur_enabled
    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)
    global current_resolution_index, fullscreen, left_key, right_key, rebinding
    while True:
        screen.blit(background, (0, 0))
        motion_blur.fill((0, 0, 0, 40))  # Transparent black for blur
        screen.blit(motion_blur, (0, 0))
        screen.blit(big_font.render("Settings", True, CYAN), (WIDTH // 2 - 80, 40))

        screen.blit(font.render("Resolution:", True, WHITE), (100, 100))
        for i, res in enumerate(RESOLUTIONS):
            text = font.render(f"{res[0]}x{res[1]}", True, WHITE)
            btn = pygame.Rect(int(250 * SCALE_X), int((90 + i * 40) * SCALE_Y), int(150 * SCALE_X), int(30 * SCALE_Y))
            pygame.draw.rect(screen, BLUE if i == current_resolution_index else GREEN, btn)
            screen.blit(text, (btn.x + 10, btn.y + 5))

        fs_text = font.render("Fullscreen: ON" if fullscreen else "Fullscreen: OFF", True, WHITE)
        fs_btn = pygame.Rect(int(100 * SCALE_X), int(300 * SCALE_Y), int(300 * SCALE_X), int(40 * SCALE_Y))
        pygame.draw.rect(screen, RED if fullscreen else GREEN, fs_btn)
        screen.blit(fs_text, fs_btn.move(10, 5))

        screen.blit(font.render("Controls:", True, WHITE), (100, 370))
        left_text = pygame.key.name(left_key)
        right_text = pygame.key.name(right_key)
        left_btn = pygame.Rect(int(250 * SCALE_X), int(370 * SCALE_Y), int(100 * SCALE_X), int(30 * SCALE_Y))
        right_btn = pygame.Rect(int(400 * SCALE_X), int(370 * SCALE_Y), int(100 * SCALE_X), int(30 * SCALE_Y))
        pygame.draw.rect(screen, BLUE, left_btn)
        pygame.draw.rect(screen, BLUE, right_btn)
        screen.blit(font.render(left_text, True, WHITE), left_btn.move(25, 5))
        screen.blit(font.render(right_text, True, WHITE), right_btn.move(25, 5))

        blur_btn = pygame.Rect(int(100 * SCALE_X), int(420 * SCALE_Y), int(300 * SCALE_X), int(40 * SCALE_Y))
        pygame.draw.rect(screen, RED if motion_blur_enabled else GREEN, blur_btn)
        blur_text = font.render("Motion Blur: ON" if motion_blur_enabled else "Motion Blur: OFF", True, WHITE)
        screen.blit(blur_text, blur_btn.move(10, 5))

        back_btn = pygame.Rect(int(100 * SCALE_X), int(470 * SCALE_Y), int(150 * SCALE_X), int(40 * SCALE_Y))
        pygame.draw.rect(screen, WHITE, back_btn)
        screen.blit(font.render("Back", True, BLACK), back_btn.move(45, 5))

        # Speech bubble for resolution note
        bubble_width = int(480 * SCALE_X)
        bubble_height = int(80 * SCALE_Y)
        bubble_x = WIDTH - bubble_width - 30
        bubble_y = int(410 * SCALE_Y)
        bubble_rect = pygame.Rect(bubble_x, bubble_y, bubble_width, bubble_height)
        pygame.draw.rect(screen, (50, 50, 50), bubble_rect, border_radius=15)
        pygame.draw.polygon(screen, (50, 50, 50), [(bubble_x + bubble_width // 2 - 10, bubble_y + bubble_height), (bubble_x + bubble_width // 2 + 10, bubble_y + bubble_height), (bubble_x + bubble_width // 2, bubble_y + bubble_height + 10)])

        note_text = font.render("keep the resolution in 1600x900 and fullscreen,", True, WHITE)
        note_text2 = font.render("we are working on the scaling (its too hard T-T)", True, WHITE)
        screen.blit(note_text, (bubble_x + 15, bubble_y + 10))
        screen.blit(note_text2, (bubble_x + 15, bubble_y + 40))

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN and rebinding:
                if rebinding == "left":
                    left_key = event.key
                elif rebinding == "right":
                    right_key = event.key
                rebinding = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, res in enumerate(RESOLUTIONS):
                    btn = pygame.Rect(250, 90 + i * 40, 150, 30)
                    if btn.collidepoint(mx, my):
                        current_resolution_index = i
                        update_resolution(current_resolution_index, fullscreen)
                if fs_btn.collidepoint(mx, my):
                    fullscreen = not fullscreen
                    update_resolution(current_resolution_index, fullscreen)
                elif left_btn.collidepoint(mx, my):
                    rebinding = "left"
                elif right_btn.collidepoint(mx, my):
                    rebinding = "right"
                elif blur_btn.collidepoint(mx, my):
                    motion_blur_enabled = not motion_blur_enabled
                elif back_btn.collidepoint(mx, my):
                    return

        pygame.display.flip()
        clock.tick(FPS)
 

# ============ GAME LOOP ============
def run_game(level=1):
    custom_cursor = pygame.image.load("cursor.png").convert_alpha()
    cursor_offset = (0, 0)  # Adjust if your image has a pointer tip not at (0,0)
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    import time
    import random
    import time
    brick_hit_count = 0
    powerup_active = False
    powerup_start_time = 0
    lives = LIVES
    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks(level)
    ball.reset_on_paddle(paddle)
    powerups = pygame.sprite.Group()
    extra_balls = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(paddle, ball)
    all_sprites.add(*bricks)

    if level == 1:
        pygame.mixer.music.load("music.mp3")
    elif level == 2:
        pygame.mixer.music.load("music2.mp3")
    elif level == 3:
        pygame.mixer.music.load("music3.mp3")
    pygame.mixer.music.play(-1)

    paused = False

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = True
            elif event.type == pygame.MOUSEMOTION:
                paddle.mouse_move(event.pos[0])
                if not ball.active:
                    ball.reset_on_paddle(paddle)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not ball.active:
                    ball.active = True

        if paused:
            resume_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 30, 200, 50)
            restart_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 40, 200, 50)
            quit_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 110, 200, 50)

            while paused:
                pygame.mouse.set_visible(True)
                screen.fill((20, 20, 20))
                screen.blit(big_font.render("Game Paused", True, CYAN), (WIDTH//2 - 160, HEIGHT//2 - 100))

                pygame.draw.rect(screen, GREEN, resume_btn, border_radius=10)
                pygame.draw.rect(screen, ORANGE, restart_btn, border_radius=10)
                pygame.draw.rect(screen, RED, quit_btn, border_radius=10)

                screen.blit(font.render("Resume", True, WHITE), resume_btn.move(55, 10))
                screen.blit(font.render("Restart", True, WHITE), restart_btn.move(50, 10))
                screen.blit(font.render("Quit to Menu", True, WHITE), quit_btn.move(30, 10))

                pygame.display.flip()

                for pause_event in pygame.event.get():
                    if pause_event.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    elif pause_event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pause_event.pos
                        if resume_btn.collidepoint((mx, my)):
                            paused = False
                            pygame.mouse.set_visible(False)
                        elif restart_btn.collidepoint((mx, my)):
                            pygame.mouse.set_visible(False)
                            return run_game(level)
                        elif quit_btn.collidepoint((mx, my)):
                            return

        all_sprites.update()
        if not ball.active:
            ball.reset_on_paddle(paddle)
        powerups.update()
        extra_balls.update()

        if ball.rect.colliderect(paddle.rect):
            # Calculate physics: ball angle based on paddle movement
            relative_intersect = (ball.rect.centerx - paddle.rect.centerx) / (paddle.rect.width / 2)
            ball.dx = int(5 * SCALE_X * relative_intersect)
            ball.dy = -abs(ball.dy)

        hit_bricks = pygame.sprite.spritecollide(ball, bricks, True)
        if hit_bricks:
            for brick in hit_bricks:
                if level == 3 and random.random() < 0.1:
                    powerup = pygame.sprite.Sprite()
                    powerup.image = pygame.Surface((20, 20))
                    powerup.image.fill((255, 255, 0))
                    powerup.rect = powerup.image.get_rect(center=brick.rect.center)
                    powerup.type = 'multi_ball'
                    powerup.speed = 3
                    powerups.add(powerup)
            brick_hit_count += len(hit_bricks)
            if level == 3 and brick_hit_count >= 20 and not powerup_active:
                powerup_active = True
                powerup_start_time = time.time()
                paddle.image = pygame.Surface((200, 20))
                paddle.image.fill(WHITE)
                paddle.rect = paddle.image.get_rect(midtop=paddle.rect.midtop)
            ball.dy *= -1

        if ball.rect.bottom >= HEIGHT:
            lives -= 1
            if lives <= 0:
                pygame.mixer.music.stop()
                decision = game_over_screen()
                if decision:
                    return run_game(level)
                else:
                    return
            ball.active = False
            ball.reset_on_paddle(paddle)


        if not bricks:
            pygame.mixer.music.stop()
            win_image = pygame.image.load("delay.jpg")
            win_image = pygame.transform.scale(win_image, (WIDTH, HEIGHT))
            for i in range(3, 0, -1):
                screen.blit(win_image, (0, 0))
                win_text = big_font.render("YOU WIN", True, BLACK)
                countdown_text = font.render(f"Returning to menu in {i}...", True, BLACK)
                screen.blit(win_text, win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
                screen.blit(countdown_text, countdown_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))
                pygame.display.flip()
                pygame.time.delay(1000)
            return "menu"

        if motion_blur_enabled:
            blur_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            blur_surface.fill((0, 0, 0, 20))  # softer blur
            screen.blit(blur_surface, (0, 0))
        else:
            screen.fill(BLACK)

        if powerup_active and time.time() - powerup_start_time > 5:
            powerup_active = False
            paddle.image = pygame.Surface((100, 20))
            paddle.image.fill(WHITE)
            paddle.rect = paddle.image.get_rect(midtop=paddle.rect.midtop)

        bricks.draw(screen)
        ball_group = pygame.sprite.Group(ball)
        ball_group.draw(screen)
        screen.blit(paddle.image, paddle.rect)
        screen.blit(font.render(f"Lives: {lives}", True, WHITE), (10, 10))
        pygame.display.flip()
        clock.tick(FPS)

# ============ MAIN MENU ============
def main_menu():
    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)
    result = None
    pygame.mixer.music.load("mainmusic.mp3")
    pygame.mixer.music.play(-1)

    level_buttons = [
        pygame.Rect(int(WIDTH // 2 - 180 * SCALE_X), int(HEIGHT // 2 - 80 * SCALE_Y), int(100 * SCALE_X), int(50 * SCALE_Y)),
        pygame.Rect(int(WIDTH // 2 - 50 * SCALE_X), int(HEIGHT // 2 - 80 * SCALE_Y), int(100 * SCALE_X), int(50 * SCALE_Y)),
        pygame.Rect(int(WIDTH // 2 + 80 * SCALE_X), int(HEIGHT // 2 - 80 * SCALE_Y), int(100 * SCALE_X), int(50 * SCALE_Y))
    ]
    settings_btn = pygame.Rect(int(WIDTH // 2 - 100 * SCALE_X), int(HEIGHT // 2), int(200 * SCALE_X), int(50 * SCALE_Y))
    quit_btn = pygame.Rect(int(WIDTH // 2 - 100 * SCALE_X), int(HEIGHT // 2 + 80 * SCALE_Y), int(200 * SCALE_X), int(50 * SCALE_Y))

    while True:
        if video:
            ret, frame = video.read()
            if not ret or frame is None:
                video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            try:
                frame = cv2.resize(frame, (WIDTH, HEIGHT))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pygame_frame = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")
                screen.blit(pygame_frame, (0, 0))
            except Exception as e:
                print(f"Video frame error: {e}")
                screen.fill(BLACK)
        else:
            screen.fill(BLACK)
        title = big_font.render("Brick Breaker", True, CYAN)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 6)))

        pygame.draw.rect(screen, (0, 200, 0), level_buttons[0], border_radius=10)  # Green
        pygame.draw.rect(screen, (128, 0, 128), level_buttons[1], border_radius=10)  # Purple
        pygame.draw.rect(screen, RED, level_buttons[2], border_radius=10)  # Red
        pygame.draw.rect(screen, BLUE, settings_btn, border_radius=10)
        pygame.draw.rect(screen, RED, quit_btn, border_radius=10)

        screen.blit(font.render("Level 1", True, WHITE), level_buttons[0].move(10, 10))
        screen.blit(font.render("Level 2", True, WHITE), level_buttons[1].move(10, 10))
        screen.blit(font.render("Level 3", True, WHITE), level_buttons[2].move(10, 10))
        settings_text = font.render("Settings", True, WHITE)
        screen.blit(settings_text, settings_text.get_rect(center=settings_btn.center))
        quit_font = pygame.font.SysFont(None, int(36 * SCALE_Y), bold=True)
        quit_text = quit_font.render("Quit", True, WHITE)
        screen.blit(quit_text, quit_text.get_rect(center=quit_btn.center))

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if level_buttons[0].collidepoint((mx, my)):
                    pygame.mixer.music.stop()
                    return run_game(level=1)
                elif level_buttons[1].collidepoint((mx, my)):
                    pygame.mixer.music.stop()
                    return run_game(level=2)
                elif level_buttons[2].collidepoint((mx, my)):
                    pygame.mixer.music.stop()
                    return run_game(level=3)
                elif settings_btn.collidepoint((mx, my)):
                    settings_menu()
                elif quit_btn.collidepoint((mx, my)):
                    return False

        pygame.display.flip()
        clock.tick(FPS)

# ============ START GAME ============
if __name__ == "__main__":
    running = True
    while running:
        result = main_menu()
        if result is False:
            running = False
    pygame.quit()
    sys.exit()

