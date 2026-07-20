class FamilyTree:
    def __init__(self, people):
        self.people = people

    # group people into generations
    def get_generations(self):
        generations = []

        def traverse(person, generation):
            if len(generations) <= generation:  # add the new generation if it doesn't exist
                generations.append([])

            if person not in generations[generation]:
                generations[generation].append(person)

            for child in person.children:
                traverse(child, generation+1)

        for root in self.get_roots():
            traverse(root, 0)
        return generations

    def get_all_people(self):
        return self.people

    def get_roots(self):
        roots = []
        for person in self.people:
            if not person.parents:
                roots.append(person)
        return roots
