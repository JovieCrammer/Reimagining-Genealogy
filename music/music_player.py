import fluidsynth
from music.note_numbers import NOTE_NUMBERS
from pathlib import Path


class MusicPlayer:
    def __init__(self):
        self.fs = fluidsynth.Synth()
        self.fs.start()
        soundfont = (Path(__file__).resolve().parent.parent
                     / "assets"
                     / "soundfonts"
                     / "GeneralUser-GS.sf2"
                     )
        sound_font_id = self.fs.sfload(str(soundfont))
        self.fs.program_select(0, sound_font_id, 0, 0)

    def play(self, note):
        midi_note = NOTE_NUMBERS[note.pitch]
        self.fs.noteon(0, midi_note, 100)

    def stop(self, note):
        midi_note = NOTE_NUMBERS[note.pitch]
        self.fs.noteoff(0, midi_note)
