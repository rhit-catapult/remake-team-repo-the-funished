import pygame
import sys
import os
from camper import Camper  # Import Camper class from camper.py

pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 512
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Scrolling Game with Camper Character")

# Load and scale background image
image_filename = "Rose-Hulman Funished background base.png"
if not os.path.exists(image_filename):
    print(f"Error: '{image_filename}' not found.")
    pygame.quit()
    sys.exit()

raw_bg = pygame.image.load(image_filename).convert()
bg_image = pygame.transform.scale(raw_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Background scroll
scroll_x = 0
scroll_speed = 4

# Character (Camper) setup
player_width = 67
player_height = 67
player_x = 100
player_y_start = SCREEN_HEIGHT - player_height - 55
player_y = player_y_start
player_speed = 5

# Create Camper object with 2 frames: idle and jump
camper = Camper(screen, player_x, player_y, ["camper_idle.png", "camper_jump.png"])

# Jumping
is_jumping = False
velocity_y = 0
gravity = 1
jump_velocity = -15
jump_ceiling = player_y_start - player_height

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    # Handle quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        camper.x += player_speed
        scroll_x -= scroll_speed
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        camper.x -= player_speed
        scroll_x += scroll_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        if not is_jumping:
            is_jumping = True
            velocity_y = jump_velocity

    # Jump + Gravity
    if is_jumping:
        player_y += velocity_y
        velocity_y += gravity

        # Jump limit
        if player_y <= jump_ceiling:
            player_y = jump_ceiling
            velocity_y = 0

        # Landing
        if player_y >= player_y_start:
            player_y = player_y_start
            is_jumping = False
            velocity_y = 0

    # Set camper's Y and animation frame
    camper.y = player_y
    camper.frames_index = 1 if is_jumping else 0  # 0 = idle, 1 = jump

    # Screen boundaries
    if camper.x < 0:
        camper.x = 0
    if camper.x + player_width > SCREEN_WIDTH:
        camper.x = SCREEN_WIDTH - player_width

    # Loop background
    if scroll_x <= -SCREEN_WIDTH:
        scroll_x = 0
    if scroll_x >= SCREEN_WIDTH:
        scroll_x = 0

    # Draw background
    screen.blit(bg_image, (scroll_x, 0))
    screen.blit(bg_image, (scroll_x + SCREEN_WIDTH, 0))

    # Draw camper character
    camper.draw()

    pygame.display.update()

pygame.quit()
sys.exit()


