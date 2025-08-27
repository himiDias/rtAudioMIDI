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

def startDetection(audio_buffer : AudioBuffer, stop_event : threading.Event):
    print("GEts here")

    block_size = 2048
    sample_rate = 44100

    while not stop_event.is_set():
        if audio_buffer.getSize() > 2048:
            print("HOLSY", flush=True)
            samples = audio_buffer.getSampleWindow()
            print(samples.size)
            #detectFrequenctYIN(samples,samplerate=sample_rate,block_size=block_size)

if __name__ == "__main__":

    array = np.load("test_samples.npy")
    
    print(array)