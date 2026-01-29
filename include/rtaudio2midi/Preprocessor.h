#ifndef PREPROCESSOR_H
#define PREPROCESSOR_H

#include <numeric>
#include <math.h>
#include <algorithm>
#include <stdlib.h>

namespace rtaudio2midi
{
    class Preprocessor
    {
    public:
        Preprocessor() {};

        void removeOffsets(float *samples, size_t count)
        {
            float sum = std::accumulate(samples, samples + count, 0.0f);
            float avg = sum / count;

            // dc offset removed
            // offset caused by hardware
            std::transform(samples, samples + count, samples,
                           [avg](float s)
                           { return s - avg; });
        }

        // filter based on instrument, for standard 4 string bass with 21 frets lowest and highest is 40Hz - 659Hz
        void highPassFiltering(float *samples, size_t count, unsigned int cut_freq, unsigned int sample_rate)
        {
            float alpha = 1.0 / (1 + 2 * M_PI * (cut_freq / sample_rate));

            for (size_t i = 0; i < count; i++)
            {
                float current_sample = samples[i];

                samples[i] = alpha * (last_output + current_sample - last_input);

                last_input = current_sample;
                last_output = samples[i];
            }
        }

        void lowPassFiltering(float *samples, size_t count, unsigned int cut_freq, unsigned int sample_rate)
        {
            float alpha = ((2.0f * M_PI * cut_freq) / sample_rate);

            for (size_t i = 0; i < count; i++)
            {
                float current_sample = samples[i];

                samples[i] = last_output + alpha * (samples[i] - last_output);

                last_input = current_sample;
                last_output = samples[i];
            }
        }

        // gate to detect when picking up noise/too quite
        // Returns true if rms strong enough to detect pitch
        // Retuns false if rms indicates noise to skip pitch detection
        bool RMSGate(float *samples, size_t count, float threshold)
        {

            std::transform(samples, samples + count, samples,
                           [](float s)
                           { return pow(s, 2.0f); });

            float sum = std::accumulate(samples, samples + count, 0.0f);
            float rms = sum / count;

            if (rms < threshold)
            {
                return false;
            }
            return true;
        }

    private:
        float last_input = 0.0f;
        float last_output = 0.0f;
    };

}

#endif