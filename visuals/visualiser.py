import pygame
from visuals.node import Node
from visuals.reveal_mode import RevealMode
from music.music_player import MusicPlayer
from music.music_generator import person_to_note
from visuals.layout_engine import LayoutEngine
from camera.camera import Camera
from visuals.glyph import Glyph


class Visualiser:
    def __init__(self, WIDTH, HEIGHT, root, reveal_mode=RevealMode.GENERATION):
        pygame.init()
        pygame.display.set_caption("Reimagining Genealogy")

        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.glyph = Glyph("assets/glyph.svg", base_size=64)

        self.nodes = []
        self.node_dictionary = {}
        self.root = root
        self.generation_lookup = {}
        self.create_generation_lookup()
        self.reveal_mode = reveal_mode
        self.node_spread = 150
        self.create_nodes()
        self.set_layout()
        self.reveal_queue = []
        self.fill_reveal_queue()
        self.last_node_time = pygame.time.get_ticks()
        self.delay = 800

        self.music_player = MusicPlayer()
        self.playing_notes = []

        self.camera = Camera(self.WIDTH, self.HEIGHT)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.camera.zoom *= 1.1
                else:
                    self.camera.zoom /= 1.1

                # Clamp zoom
                self.camera.zoom = max(0.2, min(self.camera.zoom, 5))
                print(self.camera.zoom)

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
                node.draw(self.screen, self.camera)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.event_handler()
            self.move_camera()
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

        node = Node(person, x, y, self.glyph)
        self.nodes.append(node)
        self.node_dictionary[person] = node
        return True

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

    def draw_connections(self):
        for person in self.root.get_all_people():
            child = self.node_dictionary[person]

            for parent in person.parents:
                parent_node = self.node_dictionary[parent]

                if parent_node.visible and child.visible:
                    parent_pos = self.camera.world_to_screen(
                        (parent_node.x, parent_node.y)
                    )

                    child_pos = self.camera.world_to_screen(
                        (child.x, child.y)
                    )

                    pygame.draw.line(
                        self.screen,
                        "grey18",
                        parent_pos,
                        child_pos,
                        1
                    )

    def set_layout(self):
        layout_engine = LayoutEngine(self.root, self.WIDTH, self.HEIGHT)
        positions = layout_engine.layout()

        for person, (x, y) in positions.items():
            node = self.node_dictionary[person]
            node.x = x
            node.y = y

    def move_camera(self):
        keys = pygame.key.get_pressed()
        speed = 10

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.camera.x -= speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.camera.x += speed

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.camera.y -= speed

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.camera.y += speed
