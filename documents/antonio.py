import pygame
import sys
import time
import random
class Camper:
    def __init__(self, screen, x, y, left_frames_filenames, right_frames_filenames):
        self.screen = screen
        self.x = x
        self.y = y
        self.frames = []
        self.frames_left = []
        self.frames_right = []
        self.frames_index = 0
        for file in left_frames_filenames:
            load = pygame.image.load(file)
            load = pygame.transform.scale(load, (67,67))
            self.frames_left.append(load)
        for file in right_frames_filenames:
            load = pygame.image.load(file)
            load = pygame.transform.scale(load, (67,67))
            self.frames_right.append(load)
        self.frames = self.frames_right
        self.move_time = time.time()
        self.draw_time = time.time()
    def move(self, x, y, current_time):
        if x < 0:
            self.frames = self.frames_left
        else:
            self.frames = self.frames_right
        self.x = self.x + x
        self.y = self.y + y
        if current_time - self.draw_time > 0.1:
            self.frames_index = self.frames_index + 1
            self.draw_time = current_time
            if self.frames_index >= len(self.frames):
                self.frames_index = 1
        self.move_time = current_time

    def draw(self):
        current_image = self.frames[self.frames_index]
        if time.time() - self.move_time > 0.1:
            current_image = self.frames[0]
        self.screen.blit(current_image, (self.x, self.y))

def test_character():
        # TODO: change this function to test your class
        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        clock = pygame.time.Clock()
        character = Camper(screen, 200, 200,
        ["pixil-frame-0.png", "image-frame-0.png", "image-frame-1.png", "image-frame-2.png", "image-frame-3.png", "image-frame-4.png"],
        ["pixil-frame-0.png", "pixil-frame-1.png", "pixil-frame-2.png", "pixil-frame-3.png", "pixil-frame-4.png", "pixil-frame-5.png"])
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            screen.fill("white")
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_UP]:
                character.move(0,-1,time.time())
            if pressed_keys[pygame.K_DOWN]:
                character.move(0,1,time.time())
            if pressed_keys[pygame.K_LEFT]:
                character.move(-1,0,time.time())
            if pressed_keys[pygame.K_RIGHT]:
                character.move(1,0,time.time())
            character.draw()
            pygame.display.update()

    # Testing the classes
    # click the green arrow to the left or run "Current File" in PyCharm to test this class

if __name__ == "__main__":
    test_character()




