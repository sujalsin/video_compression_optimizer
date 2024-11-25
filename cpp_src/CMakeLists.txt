cmake_minimum_required(VERSION 3.10)
project(video_optimizer)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set Python version before finding pybind11
set(Python_ROOT_DIR "/Library/Frameworks/Python.framework/Versions/3.12")
set(PYTHON_EXECUTABLE "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3")

# Set OpenCV path
set(OpenCV_DIR "/usr/local/Cellar/opencv/4.10.0_12/lib/cmake/opencv4")

# Find OpenCV package
find_package(OpenCV REQUIRED)
message(STATUS "OpenCV_INCLUDE_DIRS: ${OpenCV_INCLUDE_DIRS}")
message(STATUS "OpenCV_LIBRARIES: ${OpenCV_LIBRARIES}")

# Add pybind11
add_subdirectory(pybind11)

# Create the library
pybind11_add_module(video_processor
    video_processor.cpp
    python_bindings.cpp
)

# Include directories
target_include_directories(video_processor PRIVATE
    ${OpenCV_INCLUDE_DIRS}
    ${CMAKE_CURRENT_SOURCE_DIR}
)

# Link libraries
target_link_libraries(video_processor PRIVATE
    ${OpenCV_LIBS}
)

# Set RPATH for macOS
if(APPLE)
    set_target_properties(video_processor PROPERTIES
        BUILD_WITH_INSTALL_RPATH TRUE
        INSTALL_RPATH "@loader_path;/usr/local/Cellar/opencv/4.10.0_12/lib"
        INSTALL_NAME_DIR "@rpath"
    )
endif()
