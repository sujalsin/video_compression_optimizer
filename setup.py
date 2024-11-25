from setuptools import setup, Extension
import pybind11
import platform
import subprocess
import sys
import os

def get_opencv_info():
    # On macOS, we know the exact library location
    if platform.system() == "Darwin":
        include_dirs = ['/usr/local/include/opencv4']
        library_dirs = ['/usr/local/lib']
        libraries = ['opencv_core', 'opencv_imgproc', 'opencv_highgui', 'opencv_videoio']
        return include_dirs, library_dirs, libraries
    
    try:
        # Try to get OpenCV info from pkg-config (for other platforms)
        cflags = subprocess.check_output(['pkg-config', '--cflags', 'opencv4']).decode().strip().split()
        libs = subprocess.check_output(['pkg-config', '--libs', 'opencv4']).decode().strip().split()
        
        include_dirs = [path[2:] for path in cflags if path.startswith('-I')]
        library_dirs = [path[2:] for path in libs if path.startswith('-L')]
        libraries = [path[2:] for path in libs if path.startswith('-l')]
        
        return include_dirs, library_dirs, libraries
    except:
        # Fallback to common locations
        common_include_paths = [
            '/usr/include/opencv4',
            '/usr/local/include/opencv4'
        ]
        common_lib_paths = [
            '/usr/lib',
            '/usr/local/lib'
        ]
        opencv_libs = ['opencv_core', 'opencv_imgproc', 'opencv_highgui', 'opencv_videoio']
        
        include_dirs = [path for path in common_include_paths if os.path.isdir(path)]
        library_dirs = [path for path in common_lib_paths if os.path.isdir(path)]
        
        return include_dirs, library_dirs, opencv_libs

# Define compiler flags based on the platform
extra_compile_args = []
extra_link_args = []

if platform.system() == "Darwin":  # macOS
    extra_compile_args = ['-std=c++11']
    extra_link_args = [
        '-stdlib=libc++',
        '-rpath', '/usr/local/lib'  # Add rpath to help find OpenCV libraries at runtime
    ]

# Get OpenCV paths and libraries
opencv_include_dirs, opencv_library_dirs, opencv_libraries = get_opencv_info()
all_include_dirs = [pybind11.get_include()] + opencv_include_dirs

ext_modules = [
    Extension(
        "video_processor",
        ["cpp_src/video_processor.cpp", "cpp_src/python_bindings.cpp"],
        include_dirs=all_include_dirs,
        library_dirs=opencv_library_dirs,
        libraries=opencv_libraries,
        language='c++',
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args
    ),
]

setup(
    name="video_compression_optimizer",
    version="0.1",
    ext_modules=ext_modules,
    install_requires=[
        "pybind11>=2.6.0",
        "opencv-python>=4.0.0",
    ],
)
