
def person_to_note(person, generation):
    notes = {
        0: "c1",
        1: "c2",
        2: "c3",
        3: "c4"
    }
    return notes.get(generation)


def create_composition(root):
    generations = root.get_generations()
    for generation_number, people in enumerate(generations):
        for person in people:
            note = person_to_note(person, generation_number)
            print(f"{person.name} plays note {note}")