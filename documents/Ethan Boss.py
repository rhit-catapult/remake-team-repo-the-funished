import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ethan Boss")

Font = pygame.font.SysFont("Arial", 24)
BIG_Font = pygame.font.SysFont("Arial", 36)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (180, 180, 180)

ethan_img = pygame.image.load("ethan.png.png")
ethan_img = pygame.transform.scale(ethan_img, (250, 250))

class Fighter:
    def __init__(self, name, health, moves, x, y):
        self.name = name
        self.health = health
        self.moves = moves
        self.x = x
        self.y = y
        self.max_health = health

    def is_defeated(self):
        return self.health <= 0

    def use_move(self, move_name, target):
        move = self.moves[move_name]
        damage = random.randint(*move['damage range'])
        target.health -= damage
        target.health = max(0, target.health)
        return move_name, damage, move.get('effect', '')

player_moves = {
    "Rule Jammer": {"damage_range": (6, 14), "effect": "A rule is scrambled"},
    "Parkour": {"damage_range": (10, 18), "effect": "The counselor shakes in fear"},
    "Overclock": {"damage_range": (8, 16), "effect": "The Counselor Panics!"},
    "Grass Touch": {"damage_range": (12, 20), "effect": "Brings a tear to the counslors eye"}
}

boss_moves = {
    "Rule Enforce Beam": {"damage_range": (10, 18), "effect": "Red alert flashes!"},
    "Counselor Command": {"damage_range": (6, 12)},
    "Detention Wave": {"damage_range": (8, 15), "effect": "You feel trapped."}
}

player= Fighter("Camper", 100, player_moves, 100,350)
ethan = Fighter("Ethan", 120, boss_moves, 500,100)

def draw_health_bar(fighter, x, y, width=200, height=200):
    health_ratio = fighter.health / fighter.max_health
    pygame.draw.rect(screen, RED, (x, y, width, height))
    pygame.draw.rect(screen, GREEN, (x, y, width * health_ratio, height))

def render_text(text, x, y, color=WHITE, font=FONT):
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))

def show_move_options(selected):
    moves = list(player_moves.keys())
    for i, move in enumerate(moves):
        color = GREEN if i == selected else WHITE
        render_text(f"{i+1}. {move}", 50, 450 + i * 30, color)

def battle_loop():
    running = True
    turn = "player"
    selected_move = 0
    message = ""

    while running:
        screen.fill(BLACK)
