class Note:
    def __init__(self, pitch, duration):
        self.pitch = pitch
        self.duration = duration

    def __repr__(self):
        return f"{self.pitch} ({self.duration} beat)"
