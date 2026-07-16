from data.sample_family import root
from music.music_generator import create_composition
from music.midi_writer import write_midi


def print_tree(person, generation=0):
    print(("   " * generation) + person.name)
    for child in person.children:
        print_tree(child, generation + 1)


def print_generations():
    generations = root.get_generations()
    for generation_number, people in enumerate(generations):
        print(f"Generation {generation_number}")

        for person in people:
            print(" -", person)


print_generations()
create_composition(root)

composition = create_composition(root)
write_midi(composition)
