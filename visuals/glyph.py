import pygame


class Glyph:

    def __init__(self, png_path, base_width=40):
        self.png_path = png_path
        self.base_width = base_width

        self.image = pygame.image.load(png_path).convert_alpha()
        self.cache = {}

    def get_surface(self, zoom):
        key = round(zoom, 2)

        if key in self.cache:
            return self.cache[key]

        width = int(self.base_width * zoom)

        aspect_ratio = self.image.get_height() / self.image.get_width()
        height = int(width * aspect_ratio)

        image = pygame.transform.smoothscale(
            self.image,
            (width, height)
        )

        self.cache[key] = image

        return image