import numpy as np
import sounddevice as sd


if __name__ == "__main__":
    duration = 5 #seconds
    sd.default.samplerate =44100
    sd.default.channels = 1
    #first param is number of frames total
    print("Recording strted")
    rec = sd.rec(int(duration * sd.default.samplerate))

    sd.wait()
    print("recording done")


    if np.all(rec == 0):
        print("Silenve, detected")

    print("palying back")
    sd.play(rec)
    sd.wait()
    print("playback complete")