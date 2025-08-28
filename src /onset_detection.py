import numpy as np
import random
import threading
#import librosa
import aubio


import AudioBuffer

def detectOnset(detector,audio_block):
    onset = detector(audio_block)[0]

    onset_ms = detector.get_last_ms()
    return onset,onset_ms


def startDetection(audio_buffer : AudioBuffer, stop_event : threading.Event):
    block_size = 2048
    sample_rate = 44100


    detector_onset = aubio.onset(buf_size = block_size, hop_size = block_size,samplerate = sample_rate)
    # adjust as needed, or allow change
    # silence set high due to open mic, and background noise
    detector_onset.set_silence(-50)
    detector_onset.set_threshold(0.5)
    detector_onset.set_minioi_ms(50)

    #set adaptive whitening and or log compression later

    while not stop_event.is_set():
        if audio_buffer.getSize() > block_size:
            samples = audio_buffer.getSampleWindow()
            onset,time = detectOnset(detector_onset,samples)
            #print(onset)
            if(onset):
                print("Onset : ", onset, "| Time : ",time)


