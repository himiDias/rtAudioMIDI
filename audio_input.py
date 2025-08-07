import numpy as np
import sounddevice as sd

def audioCallback(indata , frames , time, status):
    global audio_chunk
    audio_chunk = indata[:,0]
    print(np.sqrt(np.mean(audio_chunk**2)))

def test():
    print("TESTING FUNCT2")

if __name__ == "__main__":

    # Check devices
    print(sd.default.device)


    duration = 5 #seconds
    # low sample rate for testing, this takes 2028 samples per second, and each block is 1024 samples,
    # so output is the average volume in each block, i.e two times a second
    sd.default.samplerate =2028
    sd.default.channels = 1
    sd.default.blocksize = 1024
    sd.default.dtype = 'float32'
    sd.default.latency = 'low'
    #first param is number of frames total
    test()
    stream = sd.InputStream(callback=audioCallback)

    print("Audio Stream Started")
    stream.start()

    sd.sleep(20000)

    stream.stop()
    print("Audio Stream Ended")


    print(audio_chunk)