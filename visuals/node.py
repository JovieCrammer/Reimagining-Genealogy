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

        # temporary names
        font = pygame.font.Font(None, 24)
        text = font.render(self.person.name, True, (255, 255, 255,), (0, 0, 0))
        text_rect = text.get_rect(center=(self.x, self.y + 30))
        screen.blit(text, text_rect)
