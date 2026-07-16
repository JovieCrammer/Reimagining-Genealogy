class FamilyTree:
    def __init__(self, root):
        self.root = root  # person from where exploration starts

    # group people into generations
    def get_generations(self):
        generations = []

        def traverse(person, generation):
            if len(generations) <= generation:  # add the new generation if it doesn't exist
                generations.append([])

            generations[generation].append(person)

            for child in person.children:
                traverse(child, generation+1)

        traverse(self.root, 0)
        return generations
