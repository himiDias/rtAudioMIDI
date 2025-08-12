import numpy as np
import sounddevice as sd
import threading
import time
import audio_input
import AudioBuffer


if __name__ == "__main__":

    stream_buffer = AudioBuffer.AudioBuffer(max_size=1024)

    IOThread = threading.Thread(target=audio_input.startCapture,args=(stream_buffer,))

    IOThread.start()

    IOThread.join()