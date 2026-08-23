import pygame
from visuals.node import Node
from visuals.reveal_mode import RevealMode
from music.music_player import MusicPlayer
from music.music_generator import person_to_notes
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

        self.glyph = Glyph("assets/glyph.png", base_width=40)

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
        self.motif_queue = []

        self.camera = Camera(self.WIDTH, self.HEIGHT)
        self.selected_person = None

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

        # --------------------------------------------------
        # Play musical motifs one note at a time
        # --------------------------------------------------

        for motif in self.motif_queue[:]:

            notes, node, index, next_time = motif

            if now >= next_time:

                # Stop the previous note
                if index > 0:
                    previous_note = notes[index - 1]

                    self.music_player.stop(
                        previous_note
                    )

                # Finished the motif
                if index >= len(notes):
                    node.playing = False
                    self.motif_queue.remove(motif)
                    continue

                # Play the next note
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

        # --------------------------------------------------
        # Reveal the next person
        # --------------------------------------------------

        if self.reveal_queue and now - self.last_node_time > self.delay:
            person, generation = self.reveal_queue.pop(0)

            node = self.node_dictionary[person]

            node.visible = True
            node.playing = True

            notes = person_to_notes(
                person,
                generation
            )

            self.motif_queue.append(
                (
                    notes,
                    node,
                    0,
                    now
                )
            )

            self.last_node_time = now

        # --------------------------------------------------
        # Update visible nodes
        # --------------------------------------------------

        for node in self.nodes:

            if node.visible:
                node.update()

    def draw(self):
        self.screen.fill(0)
        self.draw_connections()
        for node in self.nodes:
            if node.visible:
                node.draw(self.screen, self.camera)

        if self.selected_person is not None:
            self.draw_person_panel()
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

        # Keep track of couples we've already drawn
        drawn_couples = set()

        for person in self.root.get_all_people():

            # --------------------------------------------------
            # 1. Draw partner / parent horizontal lines
            # --------------------------------------------------

            if len(person.parents) >= 2:

                parents = tuple(
                    sorted(
                        person.parents,
                        key=lambda p: p.name
                    )
                )

                if parents not in drawn_couples:

                    # Only draw if both parents are visible
                    if all(
                            self.node_dictionary[parent].visible
                            for parent in parents
                    ):
                        parent_nodes = [
                            self.node_dictionary[parent]
                            for parent in parents
                        ]

                        parent_positions = [
                            self.camera.world_to_screen(
                                (node.x, node.y)
                            )
                            for node in parent_nodes
                        ]

                        pygame.draw.line(
                            self.screen,
                            "grey18",
                            parent_positions[0],
                            parent_positions[1],
                            1
                        )

                        drawn_couples.add(parents)

            # --------------------------------------------------
            # 2. Draw parent-couple -> child connection
            # --------------------------------------------------

            if not person.parents:
                continue

            child_node = self.node_dictionary[person]

            if not child_node.visible:
                continue

            parent_nodes = [
                self.node_dictionary[parent]
                for parent in person.parents
                if self.node_dictionary[parent].visible
            ]

            if not parent_nodes:
                continue

            # --------------------------------------------------
            # If there are two parents:
            #
            # connect the midpoint between the parents
            # to the child.
            # --------------------------------------------------

            if len(parent_nodes) >= 2:

                parent_positions = [
                    self.camera.world_to_screen(
                        (node.x, node.y)
                    )
                    for node in parent_nodes
                ]

                parent_x = sum(
                    position[0]
                    for position in parent_positions
                ) / len(parent_positions)

                parent_y = sum(
                    position[1]
                    for position in parent_positions
                ) / len(parent_positions)

                parent_centre = (
                    parent_x,
                    parent_y
                )

                child_position = self.camera.world_to_screen(
                    (child_node.x, child_node.y)
                )

                pygame.draw.line(
                    self.screen,
                    "grey18",
                    parent_centre,
                    child_position,
                    1
                )

            # --------------------------------------------------
            # If there is only one parent, connect directly.
            # --------------------------------------------------

            else:

                parent_node = parent_nodes[0]

                parent_position = self.camera.world_to_screen(
                    (parent_node.x, parent_node.y)
                )

                child_position = self.camera.world_to_screen(
                    (child_node.x, child_node.y)
                )

                pygame.draw.line(
                    self.screen,
                    "grey18",
                    parent_position,
                    child_position,
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

    def draw_person_panel(self):

        person = self.selected_person

        panel_width = 320
        panel_height = 500

        panel_x = self.WIDTH - panel_width - 30
        panel_y = 30

        # --------------------------------------------------
        # Panel background
        # --------------------------------------------------

        panel = pygame.Rect(
            panel_x,
            panel_y,
            panel_width,
            panel_height
        )

        pygame.draw.rect(
            self.screen,
            (18, 18, 18),
            panel,
            border_radius=12
        )

        pygame.draw.rect(
            self.screen,
            (70, 70, 70),
            panel,
            width=1,
            border_radius=12
        )

        # --------------------------------------------------
        # Fonts
        # --------------------------------------------------

        title_font = pygame.font.Font(None, 32)
        heading_font = pygame.font.Font(None, 22)
        body_font = pygame.font.Font(None, 20)

        x = panel_x + 25
        y = panel_y + 25

        # --------------------------------------------------
        # Name
        # --------------------------------------------------

        title = title_font.render(
            person.name,
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            title,
            (x, y)
        )

        y += 45

        # --------------------------------------------------
        # Basic information
        # --------------------------------------------------

        if person.birth_year is not None:
            text = body_font.render(
                f"Born: {person.birth_year}",
                True,
                (210, 210, 210)
            )

            self.screen.blit(text, (x, y))
            y += 28
 
        # --------------------------------------------------
        # Parents
        # --------------------------------------------------

        heading = heading_font.render(
            "Parents",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            heading,
            (x, y)
        )

        y += 25

        if person.parents:

            for parent in person.parents:
                text = body_font.render(
                    f"• {parent.name}",
                    True,
                    (190, 190, 190)
                )

                self.screen.blit(
                    text,
                    (x + 5, y)
                )

                y += 23

        else:

            text = body_font.render(
                "Unknown",
                True,
                (120, 120, 120)
            )

            self.screen.blit(
                text,
                (x + 5, y)
            )

            y += 23

        y += 12

        # --------------------------------------------------
        # Partners
        # --------------------------------------------------

        heading = heading_font.render(
            "Partner",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            heading,
            (x, y)
        )

        y += 25

        partners = self.get_partners(person)

        if partners:

            for partner in partners:
                text = body_font.render(
                    f"• {partner.name}",
                    True,
                    (190, 190, 190)
                )

                self.screen.blit(
                    text,
                    (x + 5, y)
                )

                y += 23

        else:

            text = body_font.render(
                "None recorded",
                True,
                (120, 120, 120)
            )

            self.screen.blit(
                text,
                (x + 5, y)
            )

            y += 23

        y += 12

        # --------------------------------------------------
        # Children
        # --------------------------------------------------

        heading = heading_font.render(
            "Children",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            heading,
            (x, y)
        )

        y += 25

        if person.children:

            for child in person.children:
                text = body_font.render(
                    f"• {child.name}",
                    True,
                    (190, 190, 190)
                )

                self.screen.blit(
                    text,
                    (x + 5, y)
                )

                y += 23

        else:

            text = body_font.render(
                "None recorded",
                True,
                (120, 120, 120)
            )

            self.screen.blit(
                text,
                (x + 5, y)
            )

    @staticmethod
    def get_partners(person):

        partners = []

        for child in person.children:

            for parent in child.parents:

                if parent != person and parent not in partners:
                    partners.append(parent)

        return partners
