import pygame
from visuals.node import Node


class Visualiser:
    def __init__(self, WIDTH, HEIGHT):
        pygame.init()
        pygame.display.set_caption("Reimagining Genealogy")
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.nodes = []
        self.nodes.append(Node(None, self.WIDTH/2, self.HEIGHT/2))

    @staticmethod
    def event_handler():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def update(self):
        for node in self.nodes:
            node.update()

    def draw(self):
        self.screen.fill(0)
        for node in self.nodes:
            node.draw(self.screen)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.event_handler()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()