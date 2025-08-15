import numpy as np
import sounddevice as sd
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


import audio_input
import AudioBuffer




def audio_proccesing(frame,stream_buffer : AudioBuffer):
    plt.clf()
    amplitudes =stream_buffer.getSampleWindow()
    if amplitudes.size >0:
        plt.plot(amplitudes)
        plt.ylim(-1,1)
        
     

if __name__ == "__main__":

    stream_buffer = AudioBuffer.AudioBuffer(max_size=1024, window_size= 256)
    
    stop_event = threading.Event()

    IOThread = threading.Thread(target=audio_input.startCapture,args=(stream_buffer, stop_event))

    #ProcessorThread = threading.Thread(target=audio_proccesing, args=(stream_buffer, stop_event))

    IOThread.start()

    ani = FuncAnimation(plt.gcf(),audio_proccesing,fargs=(stream_buffer,), interval=25,cache_frame_data=False)

    
    plt.tight_layout()
    plt.show()
    #ProcessorThread.start()
    stop_event.set()

    IOThread.join()

    #ProcessorThread.join()