cmake_minimum_required(VERSION 3.10)
project(RTAUDIOMIDI)

set(CMAKE_CXX_STANDARD 17)

# Include the headers folder
include_directories(include)

# Gather all source files
file(GLOB_RECURSE SOURCES "src/*.cpp")

add_executable(main ${SOURCES})

# Platform specific linking for low latency
if(APPLE)
    target_compile_definitions(main PRIVATE __MACOSX_CORE__)
    target_link_libraries(main "-framework CoreAudio" "-framework CoreFoundation")
elseif(UNIX)
    target_compile_definitions(main PRIVATE __LINUX_ALSA__)
    target_link_libraries(main asound pthread)
elseif(WIN32)
    target_compile_definitions(main PRIVATE __WINDOWS_WASAPI__)
    target_link_libraries(main ole32 dsound)
endif()