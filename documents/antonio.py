import pygame
import sys
import time
import random
class Camper:
    def __init__(self, screen, x, y, pixil_frames_filenames):
        self.screen = screen
        self.x = x
        self.y = y
        self.speed = 5
        self.frames = []
        self.frames_index = 0
        for file in pixil_frames_filenames:
            load = pygame.image.load(file)
            load = pygame.transform.scale(load, (67,67))
            self.frames.append(load)
    def move(self):
        self.x = self.x + self.speed
        self.y = self.y + self.speed
    def draw(self):
        current_image = self.frames[self.frames_index]
        self.screen.blit(current_image, (self.x, self.y))

def test_character():
        # TODO: change this function to test your class
        screen = pygame.display.set_mode((640, 480))
        character = Camper(screen, 400, 400, ["pixil-frame-0"".png"])
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            screen.fill("white")
            character.draw()
            pygame.display.update()

    # Testing the classes
    # click the green arrow to the left or run "Current File" in PyCharm to test this class

if __name__ == "__main__":
    test_character()




