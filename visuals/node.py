import pygame


class Node:
    def __init__(self, person, x, y, glyph):
        self.person = person
        self.x = x
        self.y = y
        self.glyph = glyph
        self.radius = 0
        self.target_radius = 20
        self.growth_speed = 0.2
        self.visible = False
        self.playing = False

    def update(self):
        if self.radius < self.target_radius:
            self.radius += self.growth_speed

    def draw(self, screen, camera):
        screen_x, screen_y = camera.world_to_screen((self.x, self.y))

        image = self.glyph.get_surface(camera.zoom, self.playing)

        rect = image.get_rect(center=(screen_x, screen_y))
        screen.blit(image, rect)

        # temporary names
        font = pygame.font.Font(None, 24)
        text = font.render(self.person.name, True, (255, 255, 255,), (0, 0, 0))
        text_rect = text.get_rect(center=(screen_x, screen_y + 30))
        # screen.blit(text, text_rect)
