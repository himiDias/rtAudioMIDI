import numpy as np
import librosa
import random
import threading


import AudioBuffer


min_freq = librosa.note_to_hz("F3")
max_freq = librosa.note_to_hz("C7")

def detectFrequenctYIN(audio_block, samplerate, block_size):
    f0, voiced_flags, voiced_probs = librosa.pyin(audio_block,sr=samplerate,frame_length=block_size,fmin=min_freq,fmax=max_freq)
    print("Frequency :",f0[0], "| Silence :",voiced_flags[0], "| Silence_probability :",voiced_probs[0])
    
def startDetection(audio_buffer : AudioBuffer, stop_event : threading.Event):

    pass


if __name__ == "__main__":

    array = np.load("test_samples.npy")
    
    print(array)
    detectFrequenctYIN(array, 44100,256)