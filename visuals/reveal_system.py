import pygame
from visuals.reveal_mode import RevealMode


class RevealSystem:

    def __init__(self, root, reveal_mode, delay):

        self.root = root
        self.reveal_mode = reveal_mode
        self.delay = delay

        self.reveal_queue = []
        self.last_node_time = pygame.time.get_ticks()

        self.generation_lookup = {}

        self.create_generation_lookup()
        self.fill_reveal_queue()

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

    def ready(self):

        now = pygame.time.get_ticks()

        return (
                self.reveal_queue
                and now - self.last_node_time > self.delay
        )

    def get_next(self):

        if not self.reveal_queue:
            return None

        person, generation = self.reveal_queue.pop(0)
        self.last_node_time = pygame.time.get_ticks()
        return person, generation
