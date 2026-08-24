import pygame
from models.node import Node
from reveal.reveal_system import RevealSystem
from reveal.reveal_mode import RevealMode
from music.music_player import MusicPlayer
from music.music_generator import person_to_notes
from layout.layout_engine import LayoutEngine
from camera.camera import Camera
from visuals.glyph import Glyph
from visuals.information_panel import InformationPanel
from visuals.connection_handler import ConnectionHandler


class Visualiser:
    def __init__(self, WIDTH, HEIGHT, root, reveal_mode=RevealMode.GENERATION_BIRTH_YEAR):

        # pygame
        pygame.init()
        pygame.display.set_caption("Reimagining Genealogy")

        # system
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        # glyph/s
        self.glyph = Glyph("assets/glyph.png", base_width=40)

        # nodes
        self.nodes = []
        self.node_dictionary = {}

        # tree
        self.root = root
        self.reveal_mode = reveal_mode

        # reveal
        self.delay = 800
        self.reveal_system = RevealSystem(self.root, self.reveal_mode, self.delay)

        # layout
        self.node_spread = 150
        self.create_nodes()
        self.set_layout()

        # music
        self.music_player = MusicPlayer()
        self.playing_notes = []
        self.motif_queue = []

        # camera
        self.camera = Camera(self.WIDTH, self.HEIGHT)

        # information panel
        self.selected_person = None
        self.information_panel = InformationPanel(self.WIDTH, self.HEIGHT)

        # connections
        self.connection_handler = ConnectionHandler(self.camera, self.node_dictionary)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.camera.zoom *= 1.1
                else:
                    self.camera.zoom /= 1.1

                # max/min zoom
                self.camera.zoom = max(0.2, min(self.camera.zoom, 5))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos

                    clicked_person = self.get_clicked_person(
                        mouse_x,
                        mouse_y
                    )

                    self.selected_person = clicked_person

        return True

    def update(self):
        now = pygame.time.get_ticks()

        # play note sequences
        for motif in self.motif_queue[:]:
            notes, node, index, next_time = motif
            if now >= next_time:

                # stop previous note
                if index > 0:
                    previous_note = notes[index - 1]

                    self.music_player.stop(
                        previous_note
                    )

                if index >= len(notes):
                    node.playing = False
                    self.motif_queue.remove(motif)
                    continue

                # next note
                note = notes[index]
                self.music_player.play(note)
                self.motif_queue.remove(motif)
                self.motif_queue.append(
                    (
                        notes,
                        node,
                        index + 1,
                        now + int(note.duration * 800)
                    )
                )

        if self.reveal_system.ready():
            result = self.reveal_system.get_next()

            if result is not None:
                person, generation = result
                node = self.node_dictionary[person]
                node.visible = True
                node.playing = True
                notes = person_to_notes(person, generation)
                self.motif_queue.append((notes, node, 0, now))

        for node in self.nodes:
            if node.visible:
                node.update()

    def draw(self):
        self.screen.fill(0)

        # connection lines
        self.connection_handler.draw(self.screen, self.root.get_all_people())

        for node in self.nodes:
            if node.visible:
                node.draw(self.screen, self.camera)

        # information panel
        if self.selected_person is not None:
            self.information_panel.draw(self.screen, self.selected_person)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.event_handler()
            self.camera.move()
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

    def set_layout(self):
        layout_engine = LayoutEngine(self.root, self.WIDTH, self.HEIGHT)
        positions = layout_engine.layout()

        for person, (x, y) in positions.items():
            node = self.node_dictionary[person]
            node.x = x
            node.y = y

    def get_clicked_person(self, mouse_x, mouse_y):
        for node in reversed(self.nodes):

            if not node.visible:
                continue

            screen_x, screen_y = self.camera.world_to_screen(
                (node.x, node.y)
            )

            click_radius = 30

            distance = (
                        (mouse_x - screen_x) ** 2
                        + (mouse_y - screen_y) ** 2
                       ) ** 0.5

            if distance <= click_radius:
                print(node.person)
                return node.person

        return None
