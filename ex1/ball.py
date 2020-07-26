# Ball class
import pygame
from pygame.locals import *
import random

class Ball:
    def __init__(self, x, y, vx, vy, bounds_w, bounds_h):
        self.x, self.y, self.vx, self.vy = x, y, vx, vy
        self.bounds_w, self.bounds_h = bounds_w, bounds_h

    def move(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy

        if self.x > self.bounds_w or self.x < 0:
            self.vx = -self.vx
        if self.y > self.bounds_h or self.y < 0:
            self.vy = -self.vy

class MyScene:
    def __init__(self):
        pygame.init()
        self.bounds_w, self.bounds_h = 400, 300
        self.screen = pygame.display.set_mode((self.bounds_w, self.bounds_h))
        pygame.display.set_caption("ball test")
        self.backglound_color = (0, 0, 0)
        self.ball_color = (255, 0, 0)
        self.ball_list = []
    
    def loop(self):
        self.screen.fill(self.backglound_color)
        for b in self.ball_list:
            b.move()
            # args
            # screen, color, (left position, size)
            pygame.draw.ellipse(self.screen, self.ball_color, (b.x - 5, b.y - 5, 10, 10))
    
    def touch_began(self, touch):
        x, y = touch
        vx = random.uniform(-2, 2)
        vy = random.uniform(-2, 2)
        b = Ball(x, y, vx, vy, self.bounds_w, self.bounds_h)
        self.ball_list.append(b)

if __name__ == "__main__":
    scene = MyScene()
    while(1):
        scene.loop()
        pygame.display.update()
        pygame.time.wait(30)
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                scene.touch_began(event.pos)
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                exit(0)
