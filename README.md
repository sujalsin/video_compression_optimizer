# Intelligent Video Compression Optimizer

An advanced video compression tool that uses computer vision and machine learning techniques to optimize video encoding parameters while maintaining high visual quality. The project combines Python's ease of use with C++'s performance through a hybrid architecture.

## Key Features

- **Content-Aware Compression**: Automatically analyzes video content to determine optimal compression parameters
- **Quality Metrics**: Real-time calculation of PSNR (Peak Signal-to-Noise Ratio) and SSIM (Structural Similarity Index)
- **High-Performance Processing**: C++ core with OpenCV for efficient video frame analysis
- **Python Integration**: Seamless Python bindings using pybind11
- **Adaptive Optimization**: Dynamic adjustment of compression parameters based on content complexity
- **Batch Processing**: Support for processing multiple videos with parallel execution

## Technical Architecture

### Core Components (C++)

1. **VideoProcessor Class**
   - Frame analysis and feature extraction
   - Quality metrics calculation (PSNR, SSIM)
   - Compression parameter optimization
   - OpenCV-based image processing

2. **Feature Extraction**
   - Statistical features (mean, standard deviation)
   - Edge detection metrics
   - Texture analysis using GLCM (Gray Level Co-occurrence Matrix)

3. **Parameter Optimization**
   - Dynamic bitrate adjustment
   - Resolution scaling
   - Preset selection based on content complexity

### Python Interface

- Python bindings using pybind11
- NumPy integration for efficient array operations
- High-level API for video processing

## Installation

### Prerequisites
- Python 3.12+
- C++ compiler with C++17 support
- OpenCV 4.10.0+
- CMake 3.10+

### Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/video-compression-optimizer.git
cd video-compression-optimizer
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install OpenCV (macOS):
```bash
brew install opencv
```

4. Build the C++ module:
```bash
cd cpp_src
mkdir build && cd build
cmake ..
make
```

## Project Structure

```
video_compression_optimizer/
├── cpp_src/                    # C++ source files
│   ├── video_processor.cpp     # Core video processing implementation
│   ├── video_processor.hpp     # Header file with class definitions
│   ├── python_bindings.cpp     # pybind11 bindings
│   └── CMakeLists.txt         # CMake build configuration
├── python_src/                 # Python source files
│   ├── __init__.py
│   └── video_optimizer.py      # High-level Python API
├── tests/                      # Test files
│   └── test_video_processor.py # Unit tests for video processor
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## Usage

### Python API Example
```python
from cpp_src.build.video_processor import VideoProcessor
import cv2

# Create processor instance
processor = VideoProcessor()

# Process a frame
frame = cv2.imread('input_frame.jpg')
features = processor.analyze_frame(frame)

# Get optimal compression parameters
params = processor.optimize_parameters(frame, target_quality=0.9)

# Calculate quality metrics
psnr = processor.calculate_psnr(original_frame, compressed_frame)
ssim = processor.calculate_ssim(original_frame, compressed_frame)
```

## Quality Metrics

### PSNR (Peak Signal-to-Noise Ratio)
- Measures the ratio between the maximum possible signal power and the noise power
- Higher values indicate better quality
- Typical values range from 30-50 dB

### SSIM (Structural Similarity Index)
- Measures perceived quality based on structural information
- Ranges from -1 to 1 (1 being identical images)
- More closely correlates with human perception than PSNR

## Performance Optimization

The project uses several optimization techniques:
- C++ implementation for compute-intensive operations
- OpenCV for efficient image processing
- Memory-efficient frame handling
- Parallel processing capabilities

## Development

### Building from Source
```bash
# Configure CMake build
cd cpp_src
mkdir build && cd build
cmake ..

# Build the project
make

# Run tests
cd ../..
python -m pytest tests/
```

### Adding New Features
1. Implement core functionality in C++ (cpp_src/)
2. Add Python bindings in python_bindings.cpp
3. Create Python wrapper classes if needed
4. Add unit tests in tests/
5. Update documentation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Acknowledgments

- OpenCV for computer vision capabilities
- pybind11 for seamless C++/Python integration
- The open-source community for various tools and libraries
