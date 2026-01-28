cmake_minimum_required(VERSION 3.10)
project(RTAUDIOMIDI)

set(CMAKE_CXX_STANDARD 17)

# Include the headers folder
include_directories(include
                    include/rtaudio2midi
                    ${SFML_INCLUDE_DIR})

# Gather all source files
file(GLOB_RECURSE SOURCES "src/*.cpp")

find_package(SFML 2.5 COMPONENTS graphics window system REQUIRED)

add_executable(main ${SOURCES})

# Platform specific linking for low latency
if(APPLE)
    target_compile_definitions(main PRIVATE __MACOSX_CORE__)
    target_link_libraries(main "-framework CoreAudio" "-framework CoreFoundation"
                            sfml-graphics sfml-window sfml-system)
elseif(UNIX)
    target_compile_definitions(main PRIVATE __LINUX_ALSA__)
    target_link_libraries(main asound pthread
                            sfml-graphics sfml-window sfml-system)
elseif(WIN32)
    target_compile_definitions(main PRIVATE __WINDOWS_WASAPI__)
    target_link_libraries(main ole32 dsound
                            sfml-graphics sfml-window sfml-system)
endif()