from midiutil import MIDIFile
from music.note_numbers import NOTE_NUMBERS


def write_midi(composition, filename="family.mid"):
    midi = MIDIFile(1)
    track = 0
    channel = 0
    time = 0
    tempo = 100
    midi.addTempo(track, time, tempo)

    for note in composition:
        print(note)
        midi_note = NOTE_NUMBERS[note.pitch]

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
