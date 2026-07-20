class FamilyTree:
    def __init__(self, people):
        self.people = people

    # group people into generations
    def get_generations(self):

        # Start everyone at generation 0
        generation_lookup = {
            person: 0
            for person in self.people
        }

        changed = True

        while changed:

            changed = False

            for person in self.people:

                for child in person.children:

                    # Child must be at least one generation below parent
                    if generation_lookup[child] < generation_lookup[person] + 1:
                        generation_lookup[child] = generation_lookup[person] + 1
                        changed = True

                    # Parent must be at least one generation above child
                    if generation_lookup[person] < generation_lookup[child] - 1:
                        generation_lookup[person] = generation_lookup[child] - 1
                        changed = True

        max_generation = max(generation_lookup.values())

        generations = [[] for _ in range(max_generation + 1)]

        for person, generation in generation_lookup.items():
            generations[generation].append(person)

        return generations

    def get_all_people(self):
        return self.people

    def get_roots(self):
        roots = []
        for person in self.people:
            if not person.parents:
                roots.append(person)
        return roots
