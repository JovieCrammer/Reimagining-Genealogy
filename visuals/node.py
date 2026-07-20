import pygame


class Node:
    def __init__(self, person, x, y):
        self.person = person
        self.x = x
        self.y = y
        self.radius = 0
        self.target_radius = 20
        self.growth_speed = 0.2
        self.visible = False
        self.img = pygame.image.load("assets/green_note.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (100, 80))

    def update(self):
        if self.radius < self.target_radius:
            self.radius += self.growth_speed

    def draw(self, screen):
        rect = self.img.get_rect(center=(self.x, self.y))
        screen.blit(self.img, rect)

        # temporary names
        font = pygame.font.Font(None, 24)
        text = font.render(self.person.name, True, (255, 255, 255,), (0, 0, 0))
        text_rect = text.get_rect(center=(self.x, self.y + 30))
        screen.blit(text, text_rect)
