#ifndef AUDIO_CAPTURE_H
#define AUDIO_CAPTURE_H

#include "RtAudio.h"

#include "CircularBuffer.h"

namespace rtaudio2midi
{

    class AudioCapture
    {
    public:
        AudioCapture(unsigned int sample_rate_p, unsigned int block_size_p, unsigned int channels_p);

        ~AudioCapture();

        bool start();
        bool isRunning();
        void stop();

    private:
        RtAudio audio;
        RtAudio::StreamParameters input_params;

        unsigned int sample_rate;
        unsigned int block_size;
        unsigned int channels;

        // State
        std::atomic<bool> running{false};

        // Audio buffer
        CircularBuffer<float> ring_buffer;

        // Callback
        static int audioCallback(
            void *output_buffer,
            void *input_buffer,
            unsigned int n_frames,
            double stream_time,
            RtAudioStreamStatus status,
            void *user_data);

        int processInput(void *input_buffer, unsigned int n_frames);
    };
}

#endif
