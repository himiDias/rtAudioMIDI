#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <cstring>

#include "audio_capture.h"
#include "waveform_visualiser.h"
#include "Preprocessor.h"

int main()
{
    // default values for standard monophonic audio
    const int SAMPLE_RATE = 48000;
    const int BLOCK_SIZE = 256;
    const int CHANNELS = 1;

    // Audio capturer
    rtaudio2midi::AudioCapture a_stream(SAMPLE_RATE, BLOCK_SIZE, CHANNELS);

    // Preprocessor
    rtaudio2midi::Preprocessor preprocess;

    // Display Windows
    sf::RenderWindow window(sf::VideoMode(1600, 1600), "Audio Waveform (Original vs Pre Processed)");

    sf::View topView(sf::FloatRect(0, 0, 1600, 800));
    topView.setViewport(sf::FloatRect(0.0f, 0.0f, 1.0f, 0.5f));

    sf::View bottomView(sf::FloatRect(0, 0, 1600, 800));
    bottomView.setViewport(sf::FloatRect(0.0f, 0.5f, 1.0f, 0.5f));

    // Visualisers
    rtaudio2midi::WaveformVisualiser wf_original_vis(1600, 800);
    rtaudio2midi::WaveformVisualiser wf_preprocessed_vis(1600, 800);

    // frames counts, for plotting
    const size_t CHUNK_FRAMES = 256;

    // chunks to use per plot, 16 used as bass frequencies are low
    // so need to catch multiple cycles of the waveform hence more frames per plot needed
    const size_t CHUNKS_PER_PLOT = 16;
    const size_t FRAMES_PER_PLOT = CHUNK_FRAMES * CHUNKS_PER_PLOT;

    // LOW and HIGH frequencies (set based on instrument)
    // current range is for 4 string 21 fret bass (40Hz - 660Hz) +-5 for leeway
    const int LOW_FREQ = 35;
    const int HIGH_FREQ = 665;

    // array for chunk, to be passed into getChunk
    float *chunk = new float[CHUNK_FRAMES];

    // array for frames in a single plot
    float *plot_buf = new float[FRAMES_PER_PLOT];

    size_t plot_write = 0;

    a_stream.start();

    int change = 1;
    while (a_stream.isRunning())
    {
        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
            {
                window.close();
                a_stream.stop();
            }
        }

        size_t read_count = a_stream.getNextChunk(chunk, CHUNK_FRAMES);

        if (read_count == 0)
            continue;

        std::memcpy(plot_buf + plot_write, chunk, read_count * sizeof(float));
        plot_write += read_count;

        if (plot_write >= (FRAMES_PER_PLOT))
        {
            wf_original_vis.update(plot_buf, FRAMES_PER_PLOT);

            preprocess.removeOffsets(plot_buf, plot_write);
            preprocess.highPassFiltering(plot_buf, plot_write, LOW_FREQ, SAMPLE_RATE);
            preprocess.lowPassFiltering(plot_buf, plot_write, HIGH_FREQ, SAMPLE_RATE);

            wf_preprocessed_vis.update(plot_buf, FRAMES_PER_PLOT);

            // 0.01 threshold of when to detect pitch, increase if detecting pitch when slient
            /*
            if (preprocess.RMSGate(plot_buf, plot_write, 0.005))
            {
                if (change)
                {
                    std::cout << "DETECTING PITCH" << std::endl;
                    change = 0;
                }
            }
            else
            {
                if (!change)
                {
                    change = 1;
                    std::cout << "TOO QUIET/NOISE ONLY" << std::endl;
                }
            }*/

            plot_write = 0;
        }

        window.clear(sf::Color::Black);
        window.setView(topView);
        wf_original_vis.draw(window);

        window.setView(bottomView);
        wf_preprocessed_vis.draw(window);

        window.display();
    }

    // CLEAN UP
    delete[] chunk;
    delete[] plot_buf;

    std::cout << "Build success" << std::endl;

    return EXIT_SUCCESS;
}
