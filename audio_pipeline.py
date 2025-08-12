import numpy as np
import sounddevice as sd
import threading
import time
import audio_input
import AudioBuffer


def audio_proccesing(stream_buffer : AudioBuffer, stop_event):
    while not stop_event.is_set():
        stream_buffer.getSampleWindow()
     

if __name__ == "__main__":

    stream_buffer = AudioBuffer.AudioBuffer(max_size=1024)
    
    stop_event = threading.Event()

    IOThread = threading.Thread(target=audio_input.startCapture,args=(stream_buffer, stop_event))

    ProcessorThread = threading.Thread(target=audio_proccesing, args=(stream_buffer, stop_event))

    IOThread.start()

    ProcessorThread.start()

    time.sleep(5)
    stop_event.set()

    IOThread.join()

    ProcessorThread.join()