#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include "video_processor.hpp"

namespace py = pybind11;

cv::Mat numpy_to_mat(py::array_t<uint8_t>& input) {
    py::buffer_info buf = input.request();
    if (buf.ndim != 3) {
        throw std::runtime_error("Input array must be 3-dimensional");
    }
    
    int rows = buf.shape[0];
    int cols = buf.shape[1];
    int channels = buf.shape[2];
    
    cv::Mat mat(rows, cols, CV_8UC3);
    std::memcpy(mat.data, buf.ptr, rows * cols * channels);
    return mat;
}

PYBIND11_MODULE(video_processor, m) {
    m.doc() = "Video processing optimization module"; // optional module docstring
    
    py::class_<video_optimizer::VideoProcessor::CompressionParams>(m, "CompressionParams")
        .def(py::init<>())
        .def_readwrite("bitrate", &video_optimizer::VideoProcessor::CompressionParams::bitrate)
        .def_readwrite("width", &video_optimizer::VideoProcessor::CompressionParams::width)
        .def_readwrite("height", &video_optimizer::VideoProcessor::CompressionParams::height)
        .def_readwrite("preset", &video_optimizer::VideoProcessor::CompressionParams::preset)
        .def_readwrite("target_quality", &video_optimizer::VideoProcessor::CompressionParams::target_quality)
        .def("__repr__", [](const video_optimizer::VideoProcessor::CompressionParams& p) {
            return "CompressionParams(bitrate=" + std::to_string(p.bitrate) + 
                   ", width=" + std::to_string(p.width) + 
                   ", height=" + std::to_string(p.height) + 
                   ", preset='" + p.preset + "'" +
                   ", target_quality=" + std::to_string(p.target_quality) + ")";
        });
    
    py::class_<video_optimizer::VideoProcessor>(m, "VideoProcessor")
        .def(py::init<>())
        .def("analyze_frame", [](video_optimizer::VideoProcessor& self, py::array_t<uint8_t>& input) {
            cv::Mat frame = numpy_to_mat(input);
            return self.analyzeFrame(frame);
        })
        .def("calculate_psnr", [](video_optimizer::VideoProcessor& self, 
                                 py::array_t<uint8_t>& original,
                                 py::array_t<uint8_t>& compressed) {
            cv::Mat orig = numpy_to_mat(original);
            cv::Mat comp = numpy_to_mat(compressed);
            return self.calculatePSNR(orig, comp);
        })
        .def("calculate_ssim", [](video_optimizer::VideoProcessor& self,
                                 py::array_t<uint8_t>& original,
                                 py::array_t<uint8_t>& compressed) {
            cv::Mat orig = numpy_to_mat(original);
            cv::Mat comp = numpy_to_mat(compressed);
            return self.calculateSSIM(orig, comp);
        })
        .def("optimize_parameters", [](video_optimizer::VideoProcessor& self,
                                     py::array_t<uint8_t>& frame,
                                     float target_quality) {
            cv::Mat input = numpy_to_mat(frame);
            return self.optimizeParameters(input, target_quality);
        });
}
