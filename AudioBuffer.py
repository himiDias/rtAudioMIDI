from collections import deque


class AudioBuffer:
    def __init__(self,max_size : int):
        self.buffer = deque(maxlen=max_size)
    
    def addSamples(self, new_samples):
        self.buffer.extend(new_samples)

    def getSampleWindow(self):
        print("PLACEHOLDER : Get samples from buffer")
        pass