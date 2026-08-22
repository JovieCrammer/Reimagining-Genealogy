import pygame


class Glyph:

    def __init__(self, png_path, base_width=40):
        self.png_path = png_path
        self.base_width = base_width
        self.image = pygame.image.load(png_path).convert_alpha()
        self.cache = {}
        self.glow_colour = (170, 255, 200)

    def get_surface(self, zoom, playing=False):
        key = (round(zoom, 2), playing)

        if key in self.cache:
            return self.cache[key]

        width = int(self.base_width * zoom)

        aspect_ratio = self.image.get_height() / self.image.get_width()
        height = int(width * aspect_ratio)

        image = pygame.transform.smoothscale(
            self.image,
            (width, height)
        )

        if playing:
            tint = pygame.Surface(image.get_size(), pygame.SRCALPHA)
            tint.fill(self.glow_colour)
            image.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        self.cache[key] = image
        return image
