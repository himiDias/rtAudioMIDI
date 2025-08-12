import numpy as np
import sounddevice as sd
import threading

import AudioBuffer

def makeAudioCallback(audio_buffer):
    def audioCallback(indata , frames , time, status):
        global audio_chunk
        audio_chunk = indata[:,0]
        print(np.sqrt(np.mean(audio_chunk**2)))
        audio_buffer.addSamples(audio_chunk)
    return audioCallback



#same as main
def startCapture(stream_buffer : AudioBuffer, stop_event : threading.Event):
    # Check devices
    print(sd.default.device)


    duration = 5 #seconds
    # low sample rate for testing, this takes 2028 samples per second, and each block is 1024 samples,
    # so output is the average volume in each block, i.e two times a second

    #SAMPLE RATE (ADJUST AS NEEDED), set to 44100Hz
    sd.default.samplerate =44100
    sd.default.channels = 1
    #BLOCKSIZE (ADJUST AS NEEDED), set to 256, gives 174 blocks per second
    sd.default.blocksize = 256
    sd.default.dtype = 'float32'
    sd.default.latency = 'low'
    #first param is number of frames total
    stream = sd.InputStream(callback=makeAudioCallback(stream_buffer))   

    #BUFFER SIZE (ADJUST AD NEEDED), set to 4x the block size, samples are added to buffer in blocks, buffer holds 4 blocks, each sample has a latency of 22.3ms
    #stream_buffer = AudioBuffer.AudioBuffer(max_size=1024) 

    print("Audio Stream Started")
    stream.start()

    while not stop_event.is_set():
        pass
    stream.stop()






# SUB_COMPONENT TESTING ===========================
if __name__ == "__main__":

    # Check devices
    print(sd.default.device)


    duration = 5 #seconds
    # low sample rate for testing, this takes 2028 samples per second, and each block is 1024 samples,
    # so output is the average volume in each block, i.e two times a second

    #SAMPLE RATE (ADJUST AS NEEDED), set to 44100Hz
    sd.default.samplerate =44100
    sd.default.channels = 1
    #BLOCKSIZE (ADJUST AS NEEDED), set to 256, gives 174 blocks per second
    sd.default.blocksize = 256
    sd.default.dtype = 'float32'
    sd.default.latency = 'low'
    #first param is number of frames total
    stream = sd.InputStream(callback=audioCallback)   

    #BUFFER SIZE (ADJUST AD NEEDED), set to 4x the block size, samples are added to buffer in blocks, buffer holds 4 blocks, each sample has a latency of 22.3ms
    #stream_buffer = AudioBuffer.AudioBuffer(max_size=1024) 

    print("Audio Stream Started")
    stream.start()

    sd.sleep(5000)

    stream.stop()
    print("Audio Stream Ended")
