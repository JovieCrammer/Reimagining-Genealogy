from music.note import Note


def person_to_note(person, generation):
    notes = ["C", "D", "E", "F", "G", "A", "B"]

    # pitch reflects identity (name)
    pitch = notes[len(person.name) % 7]

    # octave reflects generation
    octave = generation + 2

    # duration reflects future impact (children)
    duration = len(person.children) + 1

    return Note(pitch + str(octave), duration)


def create_composition(root):
    composition = []

    generations = root.get_generations()
    for generation_number, people in enumerate(generations):
        for person in people:
            note = person_to_note(person, generation_number)
            print(f"{person.name} plays {note}")
            composition.append(note)

    print(composition)
    return composition
