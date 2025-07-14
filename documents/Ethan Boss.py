import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boss Battle – Ethan")

# Fonts
FONT = pygame.font.SysFont("arial", 24)
BIG_FONT = pygame.font.SysFont("arial", 36)

# Colors
WHITE = (255, 255, 255)
RED = (220, 40, 40)
GREEN = (40, 200, 80)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)

# Load Ethan image
ethan_img = pygame.image.load("ethan2.png.png")
ethan_img = pygame.transform.scale(ethan_img, (190, 250))
player_img = pygame.image.load("pixil-frame-0.png")
player_img = pygame.transform.scale(player_img, (190, 250))

background_img = pygame.image.load("Background.Ethan.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Fighter class
class Fighter:
    def __init__(self, name, health, moves, x, y):
        self.name = name
        self.health = health
        self.max_health = health
        self.moves = moves
        self.x = x
        self.y = y

    def is_defeated(self):
        return self.health <= 0

    def use_move(self, move_name, target):
        move = self.moves[move_name]
        damage = random.randint(*move['damage_range'])
        target.health -= damage
        target.health = max(0, target.health)
        return move_name, damage, move.get('effect', '')

# Player and boss setup
player_moves = {
    "Hack Pulse": {"damage_range": (10, 20), "effect": "Ethan's visor flickers!"},
    "Rule Jammer": {"damage_range": (6, 16), "effect": "A rule is scrambled."},
    "Debug Strike": {"damage_range": (8, 18)},
    "Overclock": {"damage_range": (12, 30), "effect": "Massive system strain!"}
}

boss_moves = {
    "Rule Enforce Beam": {"damage_range": (10, 20), "effect": "Red alert flashes!"},
    "Counselor Command": {"damage_range": (6, 12)},
    "Funishment Wave": {"damage_range": (8, 15), "effect": "You feel trapped."}
}

player = Fighter("Camper", 100, player_moves, 100, 350)
ethan = Fighter("Ethan", 120, boss_moves, 450, 330)

# Draw health bar
def draw_health_bar(fighter, x, y, width=200, height=20):
    health_ratio = fighter.health / fighter.max_health
    pygame.draw.rect(screen, BLACK, (x - 2, y - 2, width + 4, height + 4))  # Border
    pygame.draw.rect(screen, RED, (x, y, width, height))
    pygame.draw.rect(screen, GREEN, (x, y, width * health_ratio, height))

# Render text
def render_text(text, x, y, color=WHITE, font=FONT):
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))

# Move selection interface
def show_move_options(selected):
    moves = list(player_moves.keys())

    # White box settings
    box_x = 300
    box_y = 20
    box_width = 200
    box_height = 150
    pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height))

    # Draw "Choose your move:" title
    render_text("Choose your move:", box_x + 10, box_y + 10, BLACK)

    # List the moves
    for i, move in enumerate(moves):
        color = GREEN if i == selected else BLACK
        render_text(f"{i + 1}. {move}", box_x + 10, box_y + 40 + i * 25, color)

# Game loop
def battle_loop():
    running = True
    turn = "player"
    selected_move = 0
    message = ""

    while running:
        screen.blit(background_img, (0, 0))

        # Draw characters and health
        screen.blit(ethan_img, (ethan.x, ethan.y))
        screen.blit(player_img, (player.x, player.y))
        draw_health_bar(player, 50, 50)
        draw_health_bar(ethan, 550, 50)
        render_text(f"{player.name} HP: {player.health}", 50, 25)
        render_text(f"{ethan.name} HP: {ethan.health}", 550, 25)

        # Show battle message
        if message:
            render_text(message, 50, 370, WHITE)

        # Show move menu if it's the player's turn
        if turn == "player":
            show_move_options(selected_move)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if turn == "player" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_move = (selected_move - 1) % len(player.moves)
                elif event.key == pygame.K_DOWN:
                    selected_move = (selected_move + 1) % len(player.moves)
                elif event.key == pygame.K_RETURN:
                    move_name = list(player.moves.keys())[selected_move]
                    name, damage, effect = player.use_move(move_name, ethan)
                    message = f"You used {name}! ({damage} dmg)"
                    if effect:
                        message += f" {effect}"

                    # Refresh screen to show player's move message
                    screen.blit(background_img, (0, 0))
                    screen.blit(ethan_img, (ethan.x, ethan.y))
                    screen.blit(player_img, (player.x, player.y))
                    draw_health_bar(player, 50, 50)
                    draw_health_bar(ethan, 550, 50)
                    render_text(f"{player.name} HP: {player.health}", 50, 25)
                    render_text(f"{ethan.name} HP: {ethan.health}", 550, 25)
                    render_text(message, 50, 370, WHITE)
                    pygame.display.flip()

                    pygame.time.delay(1200)
                    turn = "boss"

        if turn == "boss" and not ethan.is_defeated():
            pygame.time.delay(1000)
            move_name = random.choice(list(ethan.moves.keys()))
            name, damage, effect = ethan.use_move(move_name, player)
            message = f"Ethan used {name}! ({damage} dmg)"
            if effect:
                message += f" {effect}"
            turn = "player"
            pygame.time.delay(800)

        # Check for win/lose
        if player.is_defeated():
            render_text(" You were defeated by Ethan!", 200, 550, RED, BIG_FONT)
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False
        elif ethan.is_defeated():
            render_text(" You defeated Ethan!", 220, 550, GREEN, BIG_FONT)
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False

    pygame.quit()
    sys.exit()

# Run the fight
if __name__ == "__main__":
    battle_loop()
