import pygame
import random
import sys

pygame.init()

# Load sounds
sounds = {
    "Parkour": pygame.mixer.Sound("jump.wav"),
    "Rule Jammer": pygame.mixer.Sound("Static.mp3"),
    "Grasshole": pygame.mixer.Sound("Grass.mp3"),
    "Be Late!": pygame.mixer.Sound("Bell.mp3"),
    "Rule Enforce Beam": pygame.mixer.Sound("laserShoot.wav"),
    "Counselor Command": pygame.mixer.Sound("Yelling.mp3"),
    "Funishment Wave": pygame.mixer.Sound("Funishment.mp3")
}

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boss Battle – Ethan")

# Fonts
FONT = pygame.font.SysFont("arial", 24)
BIG_FONT = pygame.font.SysFont("arial", 30)

# Colors
WHITE = (255, 255, 255)
RED = (220, 40, 40)
GREEN = (40, 200, 80)
YELLOW = (230, 200, 20)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
SEMI_TRANSPARENT = (0, 0, 0, 150)

# Load images and scale
ethan_img = pygame.image.load("ethan2.png.png")
ethan_img = pygame.transform.scale(ethan_img, (190, 250))
player_img = pygame.image.load("pixil-frame-0.png")
player_img = pygame.transform.scale(player_img, (190, 250))
background_img = pygame.image.load("Background.Ethan.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Fighter class
class Fighter:
    def __init__(self, name, health, moves, x, y, img):
        self.name = name
        self.health = health
        self.max_health = health
        self.moves = moves
        self.x = x
        self.y = y
        self.img = img
        self.shake_offset = 0  # For attack animation
        self.current_health_display = health  # for smooth health bar animation

    def is_defeated(self):
        return self.health <= 0

    def use_move(self, move_name, target):
        move = self.moves[move_name]
        damage = random.randint(*move['damage_range'])
        target.health -= damage
        target.health = max(0, target.health)
        return move_name, damage, move.get('effect', '')

    def draw(self, surface):
        # Apply shake offset for attack effect
        offset_x = self.shake_offset
        surface.blit(self.img, (self.x + offset_x, self.y))

# Player and boss setup
player_moves = {
    "Parkour": {"damage_range": (10, 20), "effect": "Ethan shakes in fear!"},
    "Rule Jammer": {"damage_range": (6, 16), "effect": "A rule is scrambled."},
    "Grasshole": {"damage_range": (8, 18)},
    "Be Late!": {"damage_range": (12, 30), "effect": "Ethan forgets where you're at!"}
}

boss_moves = {
    "Rule Enforce Beam": {"damage_range": (10, 20), "effect": "Red alert flashes!"},
    "Counselor Command": {"damage_range": (6, 12)},
    "Funishment Wave": {"damage_range": (8, 15), "effect": "You feel trapped."}
}

player = Fighter("Camper", 100, player_moves, 70, 350, player_img)
ethan = Fighter("Ethan", 120, boss_moves, 520, 330, ethan_img)

# Utility functions

def draw_text(surface, text, x, y, color=WHITE, font=FONT):
    surf = font.render(text, True, color)
    surface.blit(surf, (x, y))

def draw_rounded_rect(surface, rect, color, corner_radius):
    """
    Draw a rectangle with rounded corners.
    """
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

def draw_health_bar(fighter, x, y, width=200, height=20):
    # Animate health bar smoothly
    speed = 1.5
    if fighter.current_health_display > fighter.health:
        fighter.current_health_display -= speed
        if fighter.current_health_display < fighter.health:
            fighter.current_health_display = fighter.health
    elif fighter.current_health_display < fighter.health:
        fighter.current_health_display += speed
        if fighter.current_health_display > fighter.health:
            fighter.current_health_display = fighter.health

    health_ratio = fighter.current_health_display / fighter.max_health
    # Color gradient: green → yellow → red
    if health_ratio > 0.6:
        bar_color = GREEN
    elif health_ratio > 0.3:
        bar_color = YELLOW
    else:
        bar_color = RED

    # Draw background and border
    pygame.draw.rect(screen, BLACK, (x - 2, y - 2, width + 4, height + 4), border_radius=8)
    pygame.draw.rect(screen, RED, (x, y, width, height), border_radius=8)
    # Draw health
    pygame.draw.rect(screen, bar_color, (x, y, int(width * health_ratio), height), border_radius=8)

    # Draw numeric health on bar
    health_text = f"{int(fighter.current_health_display)} / {fighter.max_health}"
    text_surf = FONT.render(health_text, True, BLACK)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)

    # Draw fighter name underneath health bar, centered
    name_surf = FONT.render(fighter.name, True, WHITE)
    name_rect = name_surf.get_rect(center=(x + width // 2, y + height + 22))
    screen.blit(name_surf, name_rect)

def show_move_options(selected):
    moves = list(player_moves.keys())
    box_x = 270
    box_y = 20
    box_width = 260
    box_height = 210
    box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

    # Semi-transparent background panel with rounded corners
    panel_surf = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    panel_surf.fill((30, 30, 30, 200))
    pygame.draw.rect(panel_surf, WHITE, panel_surf.get_rect(), 2, border_radius=12)
    screen.blit(panel_surf, (box_x, box_y))

    draw_text(screen, "Choose your move:", box_x + 15, box_y + 12, WHITE, font=BIG_FONT)

    for i, move in enumerate(moves):
        option_rect = pygame.Rect(box_x + 15, box_y + 50 + i * 40, box_width - 30, 35)
        if i == selected:
            pygame.draw.rect(screen, (100, 220, 100), option_rect, border_radius=8)
            pygame.draw.rect(screen, GREEN, option_rect, 2, border_radius=8)
            color = BLACK
        else:
            pygame.draw.rect(screen, (50, 50, 50), option_rect, border_radius=8)
            pygame.draw.rect(screen, WHITE, option_rect, 2, border_radius=8)
            color = WHITE

        draw_text(screen, f"{i+1}. {move}", option_rect.x + 12, option_rect.y + 6, color)

def draw_message_box(message, fade_alpha=255, inverse_colors=False):
    box_x = 50
    box_y = HEIGHT - 110
    box_width = WIDTH - 100
    box_height = 70
    message_surf = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    bg_color = (255, 255, 255, fade_alpha) if not inverse_colors else (0, 0, 0, fade_alpha)
    border_color = (0, 0, 0, fade_alpha) if not inverse_colors else (255, 255, 255, fade_alpha)
    text_color = BLACK if not inverse_colors else WHITE

    # Background box
    pygame.draw.rect(message_surf, bg_color, message_surf.get_rect(), border_radius=12)
    pygame.draw.rect(message_surf, border_color, message_surf.get_rect(), 3, border_radius=12)

    # Render message text (support multiline if needed)
    lines = message.split('\n')
    y_offset = 15
    for line in lines:
        text_surf = FONT.render(line, True, text_color)
        message_surf.blit(text_surf, (15, y_offset))
        y_offset += 28

    screen.blit(message_surf, (box_x, box_y))

def draw_turn_indicator(turn):
    if turn == "player":
        text = "Your Turn"
        color = GREEN
        x = player.x + 60
        y = player.y - 40
        pygame.draw.rect(screen, color, (x - 10, y - 5, 120, 40), border_radius=10)
        text_surf = FONT.render(text, True, WHITE)
        screen.blit(text_surf, (x, y))
    elif turn == "boss":
        text = "Ethan's Turn"
        color = RED
        x = ethan.x + 60
        y = ethan.y - 40
        pygame.draw.rect(screen, color, (x - 10, y - 5, 140, 40), border_radius=10)
        text_surf = FONT.render(text, True, WHITE)
        screen.blit(text_surf, (x, y))
    elif turn == "waiting_boss":
        # Show a bigger box above Ethan while waiting
        text = "Ethan is deciding..."
        x = ethan.x + 40
        y = ethan.y - 80

        # Create a semi-transparent surface for the box
        box_surf = pygame.Surface((160, 40), pygame.SRCALPHA)
        box_surf.fill((150, 0, 0, 180))  # dark red with alpha

        pygame.draw.rect(box_surf, (255, 80, 80), box_surf.get_rect(), 2, border_radius=10)

        screen.blit(box_surf, (x, y))
        text_surf = FONT.render(text, True, WHITE)
        text_rect = text_surf.get_rect(center=(x + 80, y + 20))
        screen.blit(text_surf, text_rect)

def player_attack_animation(fighter):
    # Shake effect
    for i in range(5):
        fighter.shake_offset = 5
        redraw_window()
        pygame.time.delay(25)
        fighter.shake_offset = -5
        redraw_window()
        pygame.time.delay(25)
    fighter.shake_offset = 0

def redraw_window():
    screen.blit(background_img, (0, 0))

    # Draw health bars on top, player on left, ethan on right
    draw_health_bar(player, 60, 40)
    draw_health_bar(ethan, 540, 40)

    # Draw fighters
    player.draw(screen)
    ethan.draw(screen)

    # Draw turn indicator
    draw_turn_indicator(turn)

    # Draw move options if it's player turn
    if turn == "player":
        show_move_options(selected_move)

    # Draw message box with current message if any
    if message:
        draw_message_box(message)

    pygame.display.flip()

clock = pygame.time.Clock()

# Game variables
turn = "player"  # or "waiting_boss", "boss", "game_over"
selected_move = 0
message = ""
wait_timer = 0
player_damaged_this_turn = False
ethans_last_move = None

# Main game loop
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
                    # Player selects move
                    move_name = list(player_moves.keys())[selected_move]

                    # Play sound if available
                    if move_name in sounds:
                        sounds[move_name].play()

                    # Player attacks Ethan
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
                # Restart game on any key
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

    # Handle Ethan's turn after 5 seconds delay
    if turn == "waiting_boss":
        now = pygame.time.get_ticks()
        if now - wait_timer > 5000:
            turn = "boss"

    if turn == "boss":
        # Ethan picks random move and attacks player
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

pygame.quit()
sys.exit()
