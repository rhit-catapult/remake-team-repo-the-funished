import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
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

class Fighter:
    def __init__(self, name, health, moves, x, y, image):
        self.name = name
        self.health = health
        self.max_health = health
        self.moves = moves
        self.x = x
        self.y = y
        self.image = image
        self.health_bar_display = health

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def use_move(self, move, target):
        move_data = self.moves[move]
        dmg = random.randint(*move_data['damage_range'])
        target.health = max(0, target.health - dmg)
        return move, dmg, move_data.get("effect", "")

player = Fighter("Camper", 100, {
    "Parkour": {"damage_range": (10, 20), "effect": "Eathan shakes in fear!"},
    "Rule Jammer": {"damage_range": (6, 16), "effect": "A rule is scrambled."},
    "Grasshole": {"damage_range": (8, 18)},
    "Be Late!": {"damage_range": (12, 30), "effect": "Eathan forgets where you're at!"}
}, 70, 330, player_img)

eathan = Fighter("Eathan", 120, {
    "Rule Enforce Beam": {"damage_range": (10, 20), "effect": "Red alert flashes!"},
    "Counselor Command": {"damage_range": (6, 12)},
    "Funishment Wave": {"damage_range": (8, 15), "effect": "You feel trapped."}
}, 520, 330, eathan_img)

clock = pygame.time.Clock()
running = True
turn = "player"
selected_move = 0
message = ""
wait_timer = 0
player_moves_list = list(player.moves.keys())
current_sound = None

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
    pygame.draw.rect(screen, (0, 255, 0) if player.health_bar_display > 60 else (255, 255, 0) if player.health_bar_display > 30 else (255, 0, 0),
                     (30, 20, int(200 * (player.health_bar_display / player.max_health)), 18))
    screen.blit(pygame.font.SysFont("arial", 18).render(f"{player.name}: {int(player.health_bar_display)}/{player.max_health}", True, (255, 255, 255)), (35, 0))

    pygame.draw.rect(screen, (0, 0, 0), (570, 20, 200, 18))
    pygame.draw.rect(screen, (0, 255, 0) if eathan.health_bar_display > 72 else (255, 255, 0) if eathan.health_bar_display > 36 else (255, 0, 0),
                     (570, 20, int(200 * (eathan.health_bar_display / eathan.max_health)), 18))
    screen.blit(pygame.font.SysFont("arial", 18).render(f"{eathan.name}: {int(eathan.health_bar_display)}/{eathan.max_health}", True, (255, 255, 255)), (575, 0))

    if turn == "player":
        pygame.draw.rect(screen, (0, 200, 0), (70, 290, 160, 30))
        screen.blit(pygame.font.SysFont("arial", 20).render("Your Turn", True, (255, 255, 255)), (90, 295))
    elif turn == "waiting":
        pygame.draw.rect(screen, (200, 0, 0), (520, 290, 180, 30))
        screen.blit(pygame.font.SysFont("arial", 20).render("Eathan is deciding...", True, (255, 255, 255)), (530, 295))

    if turn == "player":
        pygame.draw.rect(screen, (30, 30, 30), (270, 20, 260, 210))
        pygame.draw.rect(screen, (255, 255, 255), (270, 20, 260, 210), 2)
        screen.blit(pygame.font.SysFont("arial", 28).render("Choose your move:", True, (255, 255, 255)), (285, 30))
        for i, move in enumerate(player_moves_list):
            rect = pygame.Rect(285, 70 + i * 35, 230, 30)
            pygame.draw.rect(screen, (100, 100, 100) if i != selected_move else (0, 255, 100), rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)
            screen.blit(pygame.font.SysFont("arial", 20).render(f"{i+1}. {move}", True, (0, 0, 0) if i == selected_move else (255, 255, 255)), (rect.x + 10, rect.y + 5))

    if message:
        msg_lines = message.split("\n")
        pygame.draw.rect(screen, (255, 255, 255), (50, 500, 700, 80))
        pygame.draw.rect(screen, (0, 0, 0), (50, 500, 700, 80), 2)
        for i, line in enumerate(msg_lines):
            screen.blit(pygame.font.SysFont("arial", 20).render(line, True, (0, 0, 0)), (60, 510 + i * 22))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
