import numpy as np
import sounddevice as sd
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
import pyqtgraph as pg



import audio_input
import AudioBuffer




def audio_proccesing(stream_buffer : AudioBuffer):
    amplitudes =stream_buffer.getSampleWindow()
    if amplitudes.size >0:
        values_waveform.setData(amplitudes)
        
     

if __name__ == "__main__":

    stream_buffer = AudioBuffer.AudioBuffer(max_size=1024, window_size= 256)
    
    stop_event = threading.Event()

    IOThread = threading.Thread(target=audio_input.startCapture,args=(stream_buffer, stop_event))

    IOThread.start()

    
    app = QApplication(sys.argv)
    win_waveform = pg.GraphicsLayoutWidget(show = True, title = "Real-time Waveform")
    plot_waveform = win_waveform.addPlot(title="Waveform")
    values_waveform = plot_waveform.plot(pen="r")
    plot_waveform.setYRange(-1,1)

    timer = QTimer()
    timer.timeout.connect(lambda : audio_proccesing(stream_buffer=stream_buffer))
    #on timeout, audio processing is called. Timeout signal sent every 22ms
    # this is because the latency of the samples inside the buffer is roughly 22.3ms
    # so this ensures samples are processed at the same rate as samples entered into the buffer
    timer.start(22)

    app.exec_()

    stop_event.set()

    IOThread.join()