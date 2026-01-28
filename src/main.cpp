#include <stdlib.h>
#include <stdio.h>
#include <iostream>

#include <audio_capture.h>

int main()
{
    rtaudio2midi::AudioCapture a_stream(48000, 256, 1);

    a_stream.start();

    while (a_stream.isRunning())
    {
        continue;
    }

    std::cout << "Build success" << std::endl;

    return EXIT_SUCCESS;
}
