#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <cstring>

#include "audio_capture.h"
#include "waveform_visualiser.h"

int main()
{
    // Audio capturer
    rtaudio2midi::AudioCapture a_stream(48000, 256, 1);

    // Display Window
    sf::RenderWindow window(sf::VideoMode(800, 500), "Audio Waveform");

    rtaudio2midi::WaveformVisualiser wf_vis(800, 500);

    const size_t chunk_frames = 256;
    const size_t chunks_per_plot = 8;
    const size_t frames_per_plot = chunk_frames * chunks_per_plot;

    // array for chunk, to be passed into getChunk
    float *chunk = new float[chunk_frames];

    // array for frames in a single plot
    float *plot_buf = new float[frames_per_plot];

    size_t plot_write = 0;

    a_stream.start();

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

        size_t read_count = a_stream.getNextChunk(chunk, chunk_frames);

        if (read_count == 0)
            continue;

        std::memcpy(plot_buf + plot_write, chunk, read_count * sizeof(float));
        plot_write += read_count;

        if (plot_write >= (frames_per_plot))
        {
            wf_vis.update(plot_buf, frames_per_plot);
            plot_write = 0;
        }

        window.clear(sf::Color::Black);
        wf_vis.draw(window);
        window.display();
    }

    // CLEAN UP
    delete[] chunk;
    delete[] plot_buf;

    std::cout << "Build success" << std::endl;

    return EXIT_SUCCESS;
}
