#include "RtAudio.h"

#include "audio_capture.h"
#include "CircularBuffer.h"

namespace rtaudio2midi
{
    /*
    Sample_rate = 48 KHz is industry standard (audio samples/measurements per second)
    Channels (stream of samples, using 1 for monophonic audio)
    Block/Buffer size = 256 is good balance for latency and power (number of frames processed at a time, frames = samples * channels)
    */
    AudioCapture::AudioCapture(unsigned int sample_rate_p, unsigned int block_size_p, unsigned int channels_p)
    {
        sample_rate = sample_rate_p;
        block_size = block_size_p;
        channels = channels_p;

        rtaudio2midi::CircularBuffer<float> ring_buffer(block_size * 16);
    }

    bool AudioCapture::start()
    {
        if (audio.getDeviceCount() < 1)
        {
            std::cerr << "No Audio devices found!" << std::endl;
        }

        input_params.deviceId = audio.getDefaultInputDevice();
        input_params.nChannels = channels;
        input_params.firstChannel = 0;

        try
        {
            audio.openStream(nullptr,
                             &input_params,
                             RTAUDIO_FLOAT32,
                             sample_rate,
                             &block_size,
                             &audioCallback,
                             this);

            audio.startStream();

            running.store(true, std::memory_order_release);
        }
        catch (RtAudioErrorType &e)
        {
            std::cerr << "RtAudio Error Code: " << static_cast<int>(e) << std::endl;
            return false;
        }

        return true;
    }

    void AudioCapture::stop()
    {
        running.store(false, std::memory_order_release);

        if (audio.isStreamOpen())
        {
            try
            {
                if (audio.isStreamRunning())
                {
                    audio.stopStream();
                }

                audio.closeStream();
            }
            catch (...)
            {
                std::cerr << "Error closing RtAudio stream." << std::endl;
            }
        }
    }

    bool AudioCapture::isRunning() { return running; }

    int AudioCapture::audioCallback(void *output_buffer, void *input_buffer, unsigned int n_frames, double stream_time, RtAudioStreamStatus status, void *user_data)
    {
        if (status == RTAUDIO_INPUT_OVERFLOW)
        {
            std::cerr << "Warning: Input overflow" << std::endl;
        }

        AudioCapture *instance = static_cast<AudioCapture *>(user_data);

        return instance->processInput(input_buffer, n_frames);
    }

    int AudioCapture::processInput(void *input_buffer, unsigned int n_frames)
    {
        const float *chunk_samples = static_cast<const float *>(input_buffer);

        if (!ring_buffer.putChunk(chunk_samples, n_frames))
        {
            std::cerr << "Buffer Overflow : Ring buffer full, dropping " << n_frames << " incoming frames" << std::endl;
        }

        return 0;
    }

}
