import pygame
from visuals.node import Node
from visuals.reveal_mode import RevealMode
from music.music_player import MusicPlayer
from music.music_generator import person_to_note


class Visualiser:
    def __init__(self, WIDTH, HEIGHT, root, reveal_mode=RevealMode.GENERATION):
        pygame.init()
        pygame.display.set_caption("Reimagining Genealogy")
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.nodes = []
        self.node_dictionary = {}
        self.root = root
        self.generation_lookup = {}
        self.create_generation_lookup()
        self.reveal_mode = reveal_mode
        self.node_spread = 150
        self.create_nodes()
        self.layout_nodes()
        self.reveal_queue = []
        self.fill_reveal_queue()
        self.last_node_time = pygame.time.get_ticks()
        self.delay = 800
        self.music_player = MusicPlayer()
        self.playing_notes = []

    @staticmethod
    def event_handler():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def update(self):
        now = pygame.time.get_ticks()

        for note, stop_time in self.playing_notes[:]:
            if now >= stop_time:
                self.music_player.stop(note)
                self.playing_notes.remove((note, stop_time))

        if self.reveal_queue and now - self.last_node_time > self.delay:
            person, generation = self.reveal_queue.pop(0)
            node = self.node_dictionary[person]
            node.visible = True
            note = person_to_note(person, generation)

            self.music_player.play(note)
            self.playing_notes.append((note, now + note.duration * 800))
            self.last_node_time = now

        for node in self.nodes:
            if node.visible:
                node.update()

    def draw(self):
        self.screen.fill(0)
        self.draw_connections()
        for node in self.nodes:
            if node.visible:
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
        for person in self.root.get_all_people():
            self.add_node(person, self.WIDTH/2, self.HEIGHT/2)

    def add_node(self, person, x, y):
        if person in self.node_dictionary:
            return False

        node = Node(person, x, y)
        self.nodes.append(node)
        self.node_dictionary[person] = node
        return True

    def place_person(self, person, x, y, node_spread):
        created = self.add_node(person, x, y)
        if not created:
            return

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

    def fill_reveal_queue(self):
        if self.reveal_mode == RevealMode.GENERATION:
            for generation_number, people in enumerate(self.root.get_generations()):
                for person in people:
                    self.reveal_queue.append((person, generation_number))

        elif self.reveal_mode == RevealMode.BIRTH_YEAR:
            people = sorted(
                self.root.get_all_people(),
                key=lambda person: person.birth_year
            )
            for person in people:
                self.reveal_queue.append(
                    (
                        person,
                        self.generation_lookup[person]
                    )
                )

        elif self.reveal_mode == RevealMode.GENERATION_BIRTH_YEAR:
            for generation in self.root.get_generations():
                ordered = sorted(
                    generation,
                    key=lambda person: person.birth_year
                )
                for person in ordered:
                    self.reveal_queue.append(
                        (
                            person,
                            self.generation_lookup[person]
                        )
                    )

    def create_generation_lookup(self):
        generations = self.root.get_generations()
        for generation_number, people in enumerate(generations):
            for person in people:
                self.generation_lookup[person] = generation_number

    def layout_nodes(self):

        generations = self.root.get_generations()
        vertical_spacing = 120

        for generation_number, people in enumerate(generations):
            y = 100 + generation_number * vertical_spacing
            horizontal_spacing = self.WIDTH / (len(people) + 1)

            for i, person in enumerate(people):
                node = self.node_dictionary[person]
                node.x = horizontal_spacing * (i + 1)
                node.y = y

    def draw_connections(self):
        for person in self.root.get_all_people():
            child = self.node_dictionary[person]
            for parent in person.parents:
                parent_node = self.node_dictionary[parent]

                if parent_node.visible and child.visible:
                    pygame.draw.line(
                        self.screen,
                        "white",
                        (parent_node.x, parent_node.y),
                        (child.x, child.y),
                        2
                    )