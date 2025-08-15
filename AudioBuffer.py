from collections import deque
import numpy as np


class AudioBuffer:
    # max_size  : defines the number of samples the buffer can hold before circulating back
    # window_size : defines the number of samples to be removed from the buffer for processing
    def __init__(self,max_size : int, window_size : int):
        self.buffer = deque(maxlen=max_size)
        self.window_size = window_size
    
    def addSamples(self, new_samples):
        self.buffer.extend(new_samples)

    def getSampleWindow(self):
        return_samples = []
        if (not self.isEmpty()):
            for i in range(self.window_size):
                return_samples.append(self.buffer.popleft())
        
        return_samples = np.array(return_samples)
        return return_samples
    
    def isEmpty(self):
        if len(self.buffer) == 0:
            return True
        
        return False