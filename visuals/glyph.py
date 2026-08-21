import pygame


class Glyph:

    def __init__(self, png_path, base_size=64):
        self.png_path = png_path
        self.base_size = base_size

        self.image = pygame.image.load(png_path).convert_alpha()
        self.cache = {}

    def get_surface(self, zoom):
        key = round(zoom, 2)

        if key in self.cache:
            return self.cache[key]

        size = max(1, int(self.base_size * zoom))

        image = pygame.transform.smoothscale(
            self.image,
            (size, size)
        )

        self.cache[key] = image

        return image
