from data.sample_family import tree
from music.music_generator import create_composition
from music.midi_writer import write_midi
from visuals.visualiser import Visualiser
from visuals.reveal_mode import RevealMode


def print_tree(person, generation=0):
    print(("   " * generation) + person.name)
    for child in person.children:
        print_tree(child, generation + 1)


def print_generations():
    generations = tree.get_generations()
    for generation_number, people in enumerate(generations):
        print(f"Generation {generation_number}")

        for person in people:
            print(" -", person)


print_generations()
composition = create_composition(tree)
write_midi(composition)

visualiser = Visualiser(1000, 800, tree, RevealMode.GENERATION_BIRTH_YEAR)
visualiser.run()
