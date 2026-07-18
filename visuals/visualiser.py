import pygame
from visuals.node import Node


class Visualiser:
    def __init__(self, WIDTH, HEIGHT, root):
        pygame.init()
        pygame.display.set_caption("Reimagining Genealogy")
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.nodes = []
        self.root = root
        self.node_spread = 150
        self.create_nodes()
        self.visible_nodes = 0
        self.last_node_time = pygame.time.get_ticks()
        self.delay = 800

    @staticmethod
    def event_handler():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def update(self):
        now = pygame.time.get_ticks()

        if self.visible_nodes < len(self.nodes) and now - self.last_node_time > self.delay:
            self.visible_nodes += 1
            self.last_node_time = now
            
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

    def create_nodes(self):
        self.place_person(
            self.root.root,
            self.WIDTH/2,
            100,
            self.node_spread
        )

    def add_node(self, person, x, y):
        self.nodes.append(Node(person, x, y))

    def place_person(self, person, x, y, node_spread):
        self.add_node(person, x, y)
        children = person.children

        if not children:
            return

        child_y = y + 100
        num_children = len(children)

        for i, child in enumerate(children):
            child_x = x + (i - (num_children-1)/2) * node_spread

            self.place_person(
                child,
                child_x,
                child_y,
                node_spread
            )


