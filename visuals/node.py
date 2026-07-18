import pygame

class Node:
    def __init__(self, person, x, y):
        self.person = person
        self.x = x
        self.y = y
        self.radius = 0
        self.target_radius = 10
        self.growth_speed = 0.1

    def update(self):
        if self.radius < self.target_radius:
            self.radius += self.growth_speed

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(self.x), int(self.y)),
            int(self.radius)
        )
