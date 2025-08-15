import numpy as np
import sounddevice as sd
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
import random


import audio_input
import AudioBuffer


x_vals = []
y_vals = []

index = count()

def audio_proccesing(frame,stream_buffer : AudioBuffer):
    amplitudes =stream_buffer.getSampleWindow()
    if amplitudes.size >0:
        pass
        plt.plot(amplitudes)
        
     

if __name__ == "__main__":

    stream_buffer = AudioBuffer.AudioBuffer(max_size=1024, window_size= 256)
    
    stop_event = threading.Event()

    IOThread = threading.Thread(target=audio_input.startCapture,args=(stream_buffer, stop_event))

    #ProcessorThread = threading.Thread(target=audio_proccesing, args=(stream_buffer, stop_event))

    IOThread.start()

    ani = FuncAnimation(plt.gcf(),audio_proccesing,fargs=(stream_buffer,), interval=1000)

    plt.tight_layout()
    plt.show()
    #ProcessorThread.start()
    stop_event.set()

    IOThread.join()

    #ProcessorThread.join()