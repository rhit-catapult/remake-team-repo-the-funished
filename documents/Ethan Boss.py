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
ethan_img = pygame.transform.scale(ethan_img, (250, 250))

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
    "Hack Pulse": {"damage_range": (10, 18), "effect": "Ethan's visor flickers!"},
    "Rule Jammer": {"damage_range": (6, 14), "effect": "A rule is scrambled."},
    "Debug Strike": {"damage_range": (8, 16)},
    "Overclock": {"damage_range": (12, 20), "effect": "Massive system strain!"}
}

boss_moves = {
    "Rule Enforce Beam": {"damage_range": (10, 18), "effect": "Red alert flashes!"},
    "Counselor Command": {"damage_range": (6, 12)},
    "Detention Wave": {"damage_range": (8, 15), "effect": "You feel trapped."}
}

player = Fighter("Camper", 100, player_moves, 100, 350)
ethan = Fighter("Ethan", 120, boss_moves, 500, 100)

# Draw health bar
def draw_health_bar(fighter, x, y, width=200, height=20):
    health_ratio = fighter.health / fighter.max_health
    pygame.draw.rect(screen, RED, (x, y, width, height))
    pygame.draw.rect(screen, GREEN, (x, y, width * health_ratio, height))

# Render text
def render_text(text, x, y, color=WHITE, font=FONT):
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))

# Move selection interface
def show_move_options(selected):
    moves = list(player.moves.keys())
    for i, move in enumerate(moves):
        color = GREEN if i == selected else WHITE
        render_text(f"{i+1}. {move}", 50, 450 + i * 30, color)

# Game loop
def battle_loop():
    running = True
    turn = "player"
    selected_move = 0
    message = ""

    while running:
        screen.fill(BLACK)

        # Draw characters and health
        screen.blit(ethan_img, (ethan.x, ethan.y))
        draw_health_bar(player, 50, 50)
        draw_health_bar(ethan, 550, 50)
        render_text(f"{player.name} HP: {player.health}", 50, 25)
        render_text(f"{ethan.name} HP: {ethan.health}", 550, 25)

        # Show moves
        if turn == "player":
            render_text("Choose your move:", 50, 420, GRAY)
            show_move_options(selected_move)
        else:
            render_text("Ethan is choosing a move...", 50, 420, GRAY)

        # Show battle message
        if message:
            render_text(message, 50, 370, WHITE)

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
                    turn = "boss"
                    pygame.time.delay(1000)

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
