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

        bool put(T item)
        {
            size_t head = head_.load(std::memory_order_relaxed);
            size_t next_head = (head + 1) % capacity_;

            if (next_head == tail_.load(std::memory_order_acquire))
            {
                return false;
            }

            buffer_[head] = item;
            head_.store(next_head, std::memory_order_release);
            return true;
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