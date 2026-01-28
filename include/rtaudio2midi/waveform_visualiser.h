#ifndef WAVEFORM_VISUALISER_H
#define WAVEFORM_VISUALISER_H

#include <SFML/Graphics.hpp>

namespace rtaudio2midi
{
    class WaveformVisualiser
    {
    public:
        WaveformVisualiser(float width_p, float height_p)
            : width(width_p),
              height(height_p)
        {
            vertices_.setPrimitiveType(sf::LineStrip);
        }

        void update(const float *samples, size_t count)
        {
            vertices_.clear();

            for (size_t i = 0; i <= count; i++)
            {
                float x = static_cast<float>(i) * (width / count);
                float y = (height / 2.0f) + (samples[i] * (height / 2.0f));

                vertices_.append(sf::Vertex(sf::Vector2f(x, y), sf::Color::Red));
            }
        }

        void draw(sf::RenderWindow &window)
        {
            window.draw(vertices_);
        }

    private:
        float width;
        float height;

        sf::VertexArray vertices_;
    };

}

#endif