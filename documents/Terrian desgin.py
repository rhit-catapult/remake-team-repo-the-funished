import pygame
import sys
import time
import random
import Ethan_Boss
import antonio
# Game setup
def main():
    pygame.init()
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 512
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("The Funished")
    pressed_keys = pygame.key.get_pressed()
    clock = pygame.time.Clock()
    while True:
        main_game(screen,clock, SCREEN_WIDTH, SCREEN_HEIGHT)
    # Load background
def main_game(screen,clock, SCREEN_WIDTH, SCREEN_HEIGHT):
    pressed_keys = pygame.key.get_pressed()
    bg_image = pygame.image.load("Rose-Hulman Funished background base.png").convert()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Background scroll variables
    scroll_x = 0
    scroll_speed = 4
    # Camper setup
    camper_width = 67
    camper_height = 67
    camper_x = 100
    camper_y_start = SCREEN_HEIGHT - camper_height - 55
    camper_y = camper_y_start
    # Initialize Camper character
    camper = antonio.Camper(screen, camper_x, camper_y, ["pixil-frame-0.png", "pixil-frame-1.png", "pixil-frame-2.png"])

    # Movement speed
    camper_speed = 5
    running = True
    while running:
        clock.tick(60)
        current_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            dx = 0
            moving = False

        if pressed_keys[pygame.K_RIGHT]:
            dx = camper_speed
            scroll_x -= scroll_speed
            moving = True

        if pressed_keys[pygame.K_LEFT]:
            dx = -camper_speed
            moving = True  # no scroll
        # Apply movement
        camper.move(dx, 0, current_time)
        # Handle idle animation
        if not moving:
            camper.frames_index = 0  # back to idle frame
        # Horizontal movement
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            camper.move(-3, 0, time.time())
        if pressed_keys[pygame.K_RIGHT]:
            camper.move(3, 0, time.time())
        if pressed_keys[pygame.K_UP]:
            camper.move(0, -3, time.time())
        if pressed_keys[pygame.K_DOWN]:
            camper.move(0, 3, time.time())
        camper.draw()
        pygame.display.update()
        # Update camper position
        camper.y = camper_y
        camper.move(dx, 0, current_time)
        # Define Y-axis boundaries
        upper_y_limit = camper_y_start - 2 * camper_height
        lower_y_limit = camper_y_start
        # Apply vertical boundary constraints
        if camper.y < upper_y_limit:
            camper.y = upper_y_limit
            velocity_y = 0  # Optional: stop jump if exceeded
        if camper.y > lower_y_limit:
            camper.y = lower_y_limit
            is_jumping = False
            velocity_y = 0
            camper.frames_index = 0  # back to idle frame
        # Screen edge boundaries
        if camper.x < 0:
            camper.x = 0
        if camper.x + camper_width > SCREEN_WIDTH:
            camper.x = SCREEN_WIDTH - camper_width
        # Scroll background
        if pressed_keys[pygame.K_LEFT]:
            dx = -camper_speed
        if scroll_x <= -SCREEN_WIDTH:
            scroll_x = 0
        if scroll_x >= SCREEN_WIDTH:
            scroll_x = 0
        # Draw everything
        screen.blit(bg_image, (scroll_x, 0))
        screen.blit(bg_image, (scroll_x + SCREEN_WIDTH, 0))
        camper.draw()
        pygame.display.update()
def run_boss_level(screen, clock):
    global turn, selected_move, player, ethan, player_moves, boss_moves
    global player_attack_animation, redraw_window, sounds, wait_timer
    global player_damaged_this_turn, ethans_last_move, message
    running = True
    while running:
        clock.tick(60)  # 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if turn == "player":
                    if event.key == pygame.K_UP:
                        selected_move = (selected_move - 1) % len(player_moves)
                    elif event.key == pygame.K_DOWN:
                        selected_move = (selected_move + 1) % len(player_moves)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        move_name = list(player_moves.keys())[selected_move]

                        if move_name in sounds:
                            sounds[move_name].play()

                        used_move, dmg, effect = player.use_move(move_name, ethan)
                        message = f"You used {used_move}! It dealt {dmg} damage."
                        if effect:
                            message += f"\n{effect}"

                        player_attack_animation(player)
                        turn = "waiting_boss"
                        wait_timer = pygame.time.get_ticks()
                        player_damaged_this_turn = True
                        ethans_last_move = None

                elif turn == "game_over":
                    player.health = player.max_health
                    ethan.health = ethan.max_health
                    player.current_health_display = player.health
                    ethan.current_health_display = ethan.health
                    message = ""
                    turn = "player"

        # Check for game over
        if player.is_defeated():
            message = "You were defeated! Press any key to restart."
            turn = "game_over"
        elif ethan.is_defeated():
            message = "Ethan defeated! You win! Press any key to restart."
            turn = "game_over"

        # Handle Ethan's turn after delay
        if turn == "waiting_boss":
            now = pygame.time.get_ticks()
            if now - wait_timer > 5000:
                turn = "boss"

        if turn == "boss":
            move_name = random.choice(list(boss_moves.keys()))
            if move_name in sounds:
                sounds[move_name].play()

            used_move, dmg, effect = ethan.use_move(move_name, player)
            ethans_last_move = (used_move, dmg, effect)
            message = f"Ethan used {used_move}! It dealt {dmg} damage."
            if effect:
                message += f"\n{effect}"

            player_attack_animation(ethan)

            turn = "player"

        redraw_window()
main()


