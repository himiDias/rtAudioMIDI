#ifndef CIRCULAR_BUFFER_H
#define CIRCULAR_BUFFER_H

#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <memory>
#include <atomic>

namespace rtaudio2midi
{

    template <typename T>
    class CircularBuffer
    {
    public:
        explicit CircularBuffer(size_t size)
            : buffer_(new T[size], capacity_[size], head_(0), tail_(0));


        bool putChunk(const T* data, size_t count) {
            size_t head = head_.load(std::memory_order_relaxed);
            size_t tail = tail_.load(std::memory_order_acquire);

             
            size_t available = (head >= tail) ? (capacity_ - (head - tail) - 1) : (tail - head - 1);
            if (count > available) return false; 

            
            size_t spaceToEnd = capacity_ - head;
            if (count <= spaceToEnd) {
                std::copy(data, data + count, &buffer_[head]);
            } else {
                std::copy(data, data + spaceToEnd, &buffer_[head]);
                std::copy(data + spaceToEnd, data + count, &buffer_[0]);
            }
            

            head_.store((head + count) % capacity_, std::memory_order_release);
            return true;
        }

        
        size_t getChunk(T* outputArray, size_t numFrames) {
            size_t readCount = 0;
            while (readCount < numFrames) {
                if (!get(outputArray[readCount])) break;
                readCount++;
            }
            return readCount;
        }

        bool get(T &item)
        {
            size_t tail = tail_.load(std::memory_order_relaxed);

            if (tail == head_.load(std::memory_order_acquire))
            {
                return false;
            }

            item = buffer_[tail];
            tail_.store((tail + 1) % capacity_, std::memory_order_release);
            return true;
        }

    private:
        std::unique_ptr<T[]> buffer_;
        size_t capacity_;
        std::atomic<size_t> head_;
        std::atomic<size_t> tail_;
    };

}

#endif