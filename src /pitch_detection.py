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

def detectPitch(audio_block,detector):
    frequency = detector(audio_block)[0]

    return frequency

def startDetection(audio_buffer : AudioBuffer, stop_event : threading.Event):
    block_size = 2048
    sample_rate = 44100

    detector_onset = aubio.onset(buf_size = block_size, hop_size = block_size,samplerate = sample_rate)
    # adjust as needed, or allow change
    # silence set high due to open mic, and background noise
    detector_onset.set_silence(-50)
    detector_onset.set_threshold(0.5)
    detector_onset.set_minioi_ms(50)

    detector_pitch = aubio.pitch(method="yin",buf_size=block_size,hop_size=block_size,samplerate=sample_rate)

    detector_pitch.set_unit("Hz")
    detector_pitch.set_silence(-40)
    detector_pitch.set_tolerance(0.5)

    while not stop_event.is_set():
        if audio_buffer.getSize() > block_size:
            samples = audio_buffer.getSampleWindow()
            pitch = detectPitch(samples,detector_pitch)
            """
            if (len(history_five) == 3):
                hist_five_np = np.array(history_five)
                #print("Frequency | ",np.average(hist_five_np))
                history_five = []"""
            #history_five.append(pitch)

            print(pitch)

if __name__ == "__main__":

    array = np.load("test_samples.npy")
    
    #print(array)

    #print(detectPitch(array,44100,256))