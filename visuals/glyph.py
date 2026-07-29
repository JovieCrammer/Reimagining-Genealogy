import io

import cairosvg
import pygame


class Glyph:

    def __init__(self, svg_path, base_size=64):
        self.svg_path = svg_path
        self.base_size = base_size

        self.cache = {}

    def _render_svg(self, size):
        png = cairosvg.svg2png(
            url=self.svg_path,
            output_width=size,
            output_height=size
        )
        return pygame.image.load(io.BytesIO(png)).convert_alpha()

    def get_surface(self, zoom, colour):
        key = (round(zoom, 2), colour)

        if key in self.cache:
            return self.cache[key]

        size = max(1, int(self.base_size * zoom))

        surface = self._render_svg(size)

        tinted = surface.copy()
        tinted.fill(colour + (255,), special_flags=pygame.BLEND_RGBA_MULT)

        self.cache[key] = tinted

        return tinted
