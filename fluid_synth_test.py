import time
import fluidsynth


fs = fluidsynth.Synth()

fs.start()
sfid = fs.sfload("assets/soundfonts/GeneralUser-GS.sf2")
fs.program_select(0, sfid, 0, 0)

# middle C
fs.noteon(0, 60, 100)
time.sleep(2)
fs.noteoff(0, 60)
fs.delete()
