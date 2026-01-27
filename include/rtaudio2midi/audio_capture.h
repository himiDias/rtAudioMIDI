#ifndef AUDIO_CAPTURE_H
#define AUDIO_CAPTURE_H


#include "RtAudio.h"

#include "CircularBuffer.h"


namespace rtaudio2midi{

    class AudioCapture{
        public:
            AudioCapture(unsigned int sampleRate, unsigned int bufferFrames, unsigned int channels);

            ~AudioCapture();

            bool start();
            bool isRunning();
            void stop();

        private:
            RtAudio audio;
            RtAudio::StreamParameters inputParams;

            unsigned int sampleRate;
            unsigned int bufferFrames;
            unsigned int channels;

            // State
            std::atomic<bool> running{false};

            // Audio buffer
            RingBuffer<float> ringBuffer;

            // Callback
            static int audioCallback(
                void* outputBuffer,
                void* inputBuffer,
                unsigned int nFrames,
                double streamTime,
                RtAudioStreamStatus status,
                void* userData
            );

            int processInput(void* inputBuffer, unsigned int nFrames);

            static int audioCallback(void *outputBuffer, void *inputBuffer, 
                              unsigned int nBufferFrames, double streamTime, 
                              RtAudioStreamStatus status, void *userData);

    };
}


#endif
