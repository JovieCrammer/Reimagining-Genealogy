from data.sample_family import root


def print_tree(person, generation=0):
    print(("   " * generation) + person.name)
    for child in person.children:
        print_tree(child, generation + 1)


print_tree(root)
