from data.sample_family import root
from music.music_generator import create_composition
from music.midi_writer import write_midi
from visuals.visualiser import Visualiser
from visuals.reveal_mode import RevealMode


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
composition = create_composition(root)
write_midi(composition)

visualiser = Visualiser(1000, 800, root, RevealMode.BIRTH_YEAR)
visualiser.run()
