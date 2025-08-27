


class Note:
    def __init__(self,tempo,onset_time,duration,frequencies):
        self.pitch = None #would be the average of the `frequencies`, where `frequencies` is an array of frequencies captured for the duration of the note played
        self.pitch_class = None #uses the pitch calculated to get the pitch class (note symbol and the octave) e.g C3 or A#2
        self.onset = None #actual time of when note was played, to be used later to transcribe onto sheet
        self.length = None #uses the `tempo` and `duration` to calculate the length of the note, e.g full note, half note, quater note etc
        pass 

    # get average of frequencies for the frequencies detected for the duration of note
    # The set of frequencies will be gathered from the main program, not done here
    def calculatePitch(self,frequency_arr):
        pass


    #uses the pitch, and some sort of calculation and grouping to estiamte the pitch class
    def estimatePitchClass(self):
        pass

    #estimate the type of note (semibreve, minim, crochet etc). using the tempo (bpm) and the duration (ms), calculation is self explanatory
    def calculateNoteLength(self,tempo,note_duration):
        pass