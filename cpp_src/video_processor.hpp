#pragma once
#include <vector>
#include <string>
#include <memory>
#include <opencv2/opencv.hpp>

namespace video_optimizer {

class VideoProcessor {
public:
    VideoProcessor();
    ~VideoProcessor();

    // Frame processing functions
    std::vector<float> analyzeFrame(const cv::Mat& frame);
    float calculatePSNR(const cv::Mat& original, const cv::Mat& compressed);
    float calculateSSIM(const cv::Mat& original, const cv::Mat& compressed);
    
    // Compression optimization
    struct CompressionParams {
        int bitrate;
        int width;
        int height;
        std::string preset;
        float target_quality;
    };

    CompressionParams optimizeParameters(const cv::Mat& frame, float target_quality);
    
private:
    // Internal helper functions
    std::vector<float> extractFeatures(const cv::Mat& frame);
    float predictQuality(const std::vector<float>& features);
    
    // ML model weights (to be loaded from file)
    std::vector<float> model_weights_;
    
    // Cache for performance optimization
    cv::Mat working_frame_;
    std::vector<float> feature_cache_;
};

} // namespace video_optimizer
