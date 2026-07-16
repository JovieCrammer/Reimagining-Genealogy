from music.note import Note


def person_to_note(person, generation):
    notes = {
        0: "C1",
        1: "C2",
        2: "C3",
        3: "C4"
    }
    pitch = notes.get(generation)
    return Note(pitch, 1)


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
