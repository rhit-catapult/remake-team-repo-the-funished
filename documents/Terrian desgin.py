import pygame
import sys
import time
import random
import Ethan_Boss
import antonio
# Game setup
#screen = pygame.display.set_mode((800, 600))
def main():
    pygame.init()
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("The Funished")
    pressed_keys=pygame.key.get_pressed()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Eathan Boss Battle")
    # Load images
    eathan_img = pygame.transform.scale(pygame.image.load("ethan2.png.png"), (190, 250))
    player_img = pygame.transform.scale(pygame.image.load("pixil-frame-0.png"), (190, 250))
    bg_img = pygame.transform.scale(pygame.image.load("Background.Ethan.png"), (800, 600))
    # Sounds
    sounds = {
        "Parkour": pygame.mixer.Sound("jump.wav"),
        "Rule Jammer": pygame.mixer.Sound("Static.mp3"),
        "Grasshole": pygame.mixer.Sound("Grass.mp3"),
        "Be Late!": pygame.mixer.Sound("Bell.mp3"),
        "Rule Enforce Beam": pygame.mixer.Sound("laserShoot.wav"),
        "Counselor Command": pygame.mixer.Sound("Yelling.mp3"),
        "Funishment Wave": pygame.mixer.Sound("Funishment.mp3")
    }
    current_sound = None
    player = Ethan_Boss.Fighter("Camper", 100, {
        "Parkour": {"damage_range": (10, 20), "effect": "Eathan shakes in fear!"},
        "Rule Jammer": {"damage_range": (6, 16), "effect": "A rule is scrambled."},
        "Grasshole": {"damage_range": (8, 18)},
        "Be Late!": {"damage_range": (12, 30), "effect": "Eathan forgets where you're at!"}
    }, 70, 330, player_img)

    eathan = Ethan_Boss.Fighter("Eathan", 120, {
        "Rule Enforce Beam": {"damage_range": (10, 20), "effect": "Red alert flashes!"},
        "Counselor Command": {"damage_range": (6, 12)},
        "Funishment Wave": {"damage_range": (8, 15), "effect": "You feel trapped."}}, 520, 330, eathan_img)
    player_moves_list = list(player.moves.keys())
    selected_move = 0
    message = ""

    Boss_fight_started = False
    turn = "player"
    while True:
        pressed_keys = pygame.key.get_pressed()
        main_game(screen,clock, SCREEN_WIDTH, SCREEN_HEIGHT)
        run_boss_level(screen, clock, sounds, eathan, player, bg_img, turn, eathan_img, player_img, player_moves_list, selected_move, message, current_sound)
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
    camper = antonio.Camper(screen, camper_x, camper_y,
    ["pixil-frame-0.png", "image-frame-0.png", "image-frame-1.png", "image-frame-2.png", "image-frame-3.png", "image-frame-4.png"],
    ["pixil-frame-0.png", "pixil-frame-1.png", "pixil-frame-2.png", "pixil-frame-3.png", "pixil-frame-4.png", "pixil-frame-5.png"])
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
        if scroll_x <= -600:
            running = False
        print(scroll_x)
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

def run_boss_level(screen, clock, sounds, eathan, player, bg_img, turn, eathan_img, player_img, player_moves_list, selected_move, message, current_sound):
    global player_attack_animation, redraw_window, wait_timer
    global player_damaged_this_turn, ethans_last_move
    running = True
    while running:
        screen.blit(bg_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and turn == "player":
                if event.key == pygame.K_UP:
                    selected_move = (selected_move - 1) % len(player_moves_list)
                elif event.key == pygame.K_DOWN:
                    selected_move = (selected_move + 1) % len(player_moves_list)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if current_sound:
                        current_sound.stop()
                    move_name = player_moves_list[selected_move]
                    if move_name in sounds:
                        current_sound = sounds[move_name]
                        current_sound.play()
                    move, dmg, effect = player.use_move(move_name, eathan)
                    message = f"You used {move}! It dealt {dmg} damage.\n{effect}"
                    turn = "waiting"
                    wait_timer = pygame.time.get_ticks()

        if turn == "waiting" and pygame.time.get_ticks() - wait_timer > 2000:
            if current_sound:
                current_sound.stop()
            move_name = random.choice(list(eathan.moves.keys()))
            if move_name in sounds:
                current_sound = sounds[move_name]
                current_sound.play()
            move, dmg, effect = eathan.use_move(move_name, player)
            message = f"Eathan used {move}! It dealt {dmg} damage.\n{effect}"
            turn = "player"

        if player.health <= 0:
            message = "You were defeated by Eathan!"
            turn = "end"
        elif eathan.health <= 0:
            message = "You defeated Eathan!"
            turn = "end"

        if player.health_bar_display > player.health:
            player.health_bar_display -= 0.8
        if eathan.health_bar_display > eathan.health:
            eathan.health_bar_display -= 0.8

        player.draw(screen)
        eathan.draw(screen)

        # Small health bars, repositioned further apart
        pygame.draw.rect(screen, (0, 0, 0), (30, 20, 200, 18))
        pygame.draw.rect(screen, (0, 255, 0) if player.health_bar_display > 60 else (255, 255,
                                                                                     0) if player.health_bar_display > 30 else (
            255, 0, 0),
                         (30, 20, int(200 * (player.health_bar_display / player.max_health)), 18))
        screen.blit(pygame.font.SysFont("arial", 18).render(
            f"{player.name}: {int(player.health_bar_display)}/{player.max_health}", True, (255, 255, 255)), (35, 0))

        pygame.draw.rect(screen, (0, 0, 0), (570, 20, 200, 18))
        pygame.draw.rect(screen, (0, 255, 0) if eathan.health_bar_display > 72 else (255, 255,
                                                                                     0) if eathan.health_bar_display > 36 else (
            255, 0, 0),
                         (570, 20, int(200 * (eathan.health_bar_display / eathan.max_health)), 18))
        screen.blit(pygame.font.SysFont("arial", 18).render(
            f"{eathan.name}: {int(eathan.health_bar_display)}/{eathan.max_health}", True, (255, 255, 255)), (575, 0))

        if turn == "player":
            pygame.draw.rect(screen, (0, 200, 0), (70, 290, 160, 30))
            screen.blit(pygame.font.SysFont("arial", 20).render("Your Turn", True, (255, 255, 255)), (90, 295))
        elif turn == "waiting":
            pygame.draw.rect(screen, (200, 0, 0), (520, 290, 180, 30))
            screen.blit(pygame.font.SysFont("arial", 20).render("Eathan is deciding...", True, (255, 255, 255)),
                        (530, 295))
        if turn == "end":
            render = pygame.font.SysFont("arial", 100).render("Game Over", True, (255, 255, 255))
            screen.blit(render, (screen.get_width()/2 - render.get_width()/2, 50))
            current_sound.stop()
            if player.health > 0:
                render = pygame.font.SysFont("arial", 50).render("You Win", True, (255, 255, 255))
                screen.blit(render, (screen.get_width() / 2 - render.get_width() / 2, 160))



        if turn == "player":
            pygame.draw.rect(screen, (30, 30, 30), (270, 20, 260, 210))
            pygame.draw.rect(screen, (255, 255, 255), (270, 20, 260, 210), 2)
            screen.blit(pygame.font.SysFont("arial", 28).render("Choose your move:", True, (255, 255, 255)), (285, 30))
            for i, move in enumerate(player_moves_list):
                rect = pygame.Rect(285, 70 + i * 35, 230, 30)
                pygame.draw.rect(screen, (100, 100, 100) if i != selected_move else (0, 255, 100), rect)
                pygame.draw.rect(screen, (255, 255, 255), rect, 2)
                screen.blit(pygame.font.SysFont("arial", 20).render(f"{i + 1}. {move}", True,
                                                                    (0, 0, 0) if i == selected_move else (255, 255,
                                                                                                          255)),
                            (rect.x + 10, rect.y + 5))

        if message:
            msg_lines = message.split("\n")
            pygame.draw.rect(screen, (255, 255, 255), (50, 500, 700, 80))
            pygame.draw.rect(screen, (0, 0, 0), (50, 500, 700, 80), 2)
            for i, line in enumerate(msg_lines):
                screen.blit(pygame.font.SysFont("arial", 20).render(line, True, (0, 0, 0)), (60, 510 + i * 22))

        pygame.display.flip()
        clock.tick(60)
        # return turn
main()


