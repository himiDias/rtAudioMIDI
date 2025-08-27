import numpy as np
import random
import threading
#import librosa
import aubio


import AudioBuffer

"""
min_freq = librosa.note_to_hz("F3")
max_freq = librosa.note_to_hz("C7")

def detectFrequenctYIN(audio_block, samplerate, block_size):
    print("Detection started")
    f0, voiced_flags, voiced_probs = librosa.pyin(audio_block,sr=samplerate,frame_length=block_size,fmin=min_freq,fmax=max_freq)
    print("pyin returned,",f0,flush=True)
    print("Frequency :",f0[0], "| Silence :",voiced_flags[0], "| Silence_probability :",voiced_probs[0], flush=True)
"""

def detectPitch(audio_block,samplerate,block_size):
    detector = aubio.pitch(method="yin",buf_size=block_size,hop_size=block_size,samplerate=samplerate)

    detector.set_unit("Hz")
    detector.set_silence(-40)
    detector.set_tolerance(0.5)

    frequency = detector(audio_block)[0]

    return frequency

def startDetection(audio_buffer : AudioBuffer, stop_event : threading.Event):
    block_size = 2048
    sample_rate = 44100

    history_five = []

    while not stop_event.is_set():
        if audio_buffer.getSize() > block_size:
            samples = audio_buffer.getSampleWindow()
            pitch = detectPitch(samples,samplerate=sample_rate,block_size=block_size)
            if (len(history_five) == 3):
                hist_five_np = np.array(history_five)
                #print("Frequency | ",np.average(hist_five_np))
                history_five = []
            history_five.append(pitch)

            print(pitch)

if __name__ == "__main__":

    array = np.load("test_samples.npy")
    
    #print(array)

    #print(detectPitch(array,44100,256))