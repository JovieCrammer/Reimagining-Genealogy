from music.note import Note


# Notes available to the musical system
NOTE_NAMES = ["C", "D", "E", "F", "G", "A", "B"]


def root_motif(person):
    """
    Give a person who has no parents their own
    three-note musical identity.

    This is deterministic, so the same person always
    gets the same motif.
    """

    name_value = sum(ord(char) for char in person.name)

    first = NOTE_NAMES[name_value % 7]
    second = NOTE_NAMES[(name_value // 7 + 2) % 7]
    third = NOTE_NAMES[(name_value // 13 + 4) % 7]

    return [first, second, third]


def inherit_motif(parent_a, parent_b):
    """
    Combine two parent motifs.

    Each position in the child's motif inherits from
    one of the parents.

    Example:

        Parent A = A E G
        Parent B = B A E

        Child    = A A G
    """

    return [
        parent_a[0],
        parent_b[1],
        parent_a[2]
    ]


def inherit_from_one_parent(parent_motif):
    """
    If only one parent is known, inherit mostly from
    that parent's motif while introducing a small
    musical variation.
    """

    motif = parent_motif.copy()

    # Move the middle note one step in the scale.
    index = NOTE_NAMES.index(motif[1])
    motif[1] = NOTE_NAMES[(index + 1) % len(NOTE_NAMES)]

    return motif


def motif_pitch(motif_note, generation):
    """
    Convert a pitch class such as 'A' into a MIDI-style
    pitch name such as 'A4'.

    Generation controls the octave, so the musical
    material rises through the family tree.
    """

    octave = generation + 3

    return motif_note + str(octave)


def person_to_motif(person, generation, cache=None):

    if cache is None:
        cache = {}

    # Avoid calculating the same person's motif twice.
    if person in cache:
        return cache[person]

    # --------------------------------------------------
    # No parents = musical origin
    # --------------------------------------------------

    if not person.parents:

        motif = root_motif(person)

    # --------------------------------------------------
    # One known parent
    # --------------------------------------------------

    elif len(person.parents) == 1:

        parent = person.parents[0]

        parent_motif = person_to_motif(
            parent,
            generation - 1,
            cache
        )

        motif = inherit_from_one_parent(
            parent_motif
        )

    # --------------------------------------------------
    # Two or more parents
    # --------------------------------------------------

    else:

        parent_a = person.parents[0]
        parent_b = person.parents[1]

        motif_a = person_to_motif(
            parent_a,
            generation - 1,
            cache
        )

        motif_b = person_to_motif(
            parent_b,
            generation - 1,
            cache
        )

        motif = inherit_motif(
            motif_a,
            motif_b
        )

    cache[person] = motif

    return motif


def person_to_notes(person, generation, cache=None):

    motif = person_to_motif(
        person,
        generation,
        cache
    )

    return [
        Note(
            motif_pitch(note, generation),
            0.4
        )
        for note in motif
    ]


def create_composition(root):

    composition = []
    cache = {}

    generations = root.get_generations()

    for generation_number, people in enumerate(generations):

        for person in people:

            notes = person_to_notes(
                person,
                generation_number,
                cache
            )

            print(
                f"{person.name} plays "
                f"{[note.pitch for note in notes]}"
            )

            composition.extend(notes)

    print(composition)

    return composition