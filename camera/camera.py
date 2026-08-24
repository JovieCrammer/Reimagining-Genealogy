import pygame


class Camera:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.x = width/2
        self.y = height/2
        self.zoom = 1.0

    def world_to_screen(self, pos):
        x, y = pos
        return (
                (x - self.x) * self.zoom + self.w/2,
                (y - self.y) * self.zoom + self.h/2,
        )

    def scale(self, image):
        w = int(image.get_width() * self.zoom)
        h = int(image.get_height() * self.zoom)

        return pygame.transform.smoothscale(image, (w, h))

    def move(self):
        keys = pygame.key.get_pressed()
        speed = 10

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += speed

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= speed

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += speed
