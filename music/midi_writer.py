from midiutil import MIDIFile

def write_midi(composition, filename="family.mid"):
    midi = MIDIFile(1)

    track = 0
    channel = 0
    time = 0
    tempo = 100
    midi.addTempo(track, time, tempo)

    note_numbers = {
        "C1": 24,
        "D1": 26,
        "E1": 28,
        "F1": 29,
        "G1": 31,
        "A1": 33,
        "B1": 35,

        "C2": 36,
        "D2": 38,
        "E2": 40,
        "F2": 41,
        "G2": 43,
        "A2": 45,
        "B2": 47,

        "C3": 48,
        "D3": 50,
        "E3": 52,
        "F3": 53,
        "G3": 55,
        "A3": 57,
        "B3": 59,

        "C4": 60,
        "D4": 62,
        "E4": 64,
        "F4": 65,
        "G4": 67,
        "A4": 69,
        "B4": 71,
    }

    for note in composition:
        print(note)
        midi_note = note_numbers[note.pitch]

        midi.addNote(
            track,
            channel,
            midi_note,
            time,
            note.duration,
            volume=100
        )
        time += note.duration

    with open(filename, "wb") as output:
        midi.writeFile(output)
