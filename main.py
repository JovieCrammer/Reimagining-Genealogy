from data.sample_family import root


def print_tree(person, generation=0):
    print(("   " * generation) + person.name)
    for child in person.children:
        print_tree(child, generation + 1)


def print_generations():
    generations = root.get_generations()
    for number, people in enumerate(generations):
        print(f"Generation{number}")

        for person in people:
            print(" -", person)


print_generations()

