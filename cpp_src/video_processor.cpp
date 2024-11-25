#include "video_processor.hpp"
#include <cmath>
#include <algorithm>
#include <numeric>

using std::vector;
using std::string;
using std::min;
using std::max;
using std::accumulate;

namespace video_optimizer {

VideoProcessor::VideoProcessor() {
    // Initialize model weights (in practice, these would be loaded from a file)
    model_weights_ = vector<float>(128, 1.0f);
}

VideoProcessor::~VideoProcessor() = default;

vector<float> VideoProcessor::analyzeFrame(const cv::Mat& frame) {
    // Keep original frame for edge detection
    working_frame_ = frame.clone();
    
    // Extract features
    return extractFeatures(working_frame_);
}

float VideoProcessor::calculatePSNR(const cv::Mat& original, const cv::Mat& compressed) {
    cv::Mat diff;
    cv::absdiff(original, compressed, diff);
    diff.convertTo(diff, CV_32F);
    diff = diff.mul(diff);
    
    float mse = static_cast<float>(cv::sum(diff)[0]) / (diff.cols * diff.rows);
    if (mse <= 1e-10) return 100.0f;
    
    return 20 * log10(1.0f / sqrt(mse));
}

float VideoProcessor::calculateSSIM(const cv::Mat& original, const cv::Mat& compressed) {
    const float C1 = 6.5025f;  // (0.01 * 255)^2
    const float C2 = 58.5225f; // (0.03 * 255)^2
    
    cv::Mat img1, img2;
    original.convertTo(img1, CV_32F);
    compressed.convertTo(img2, CV_32F);
    
    cv::Mat mu1, mu2;
    cv::GaussianBlur(img1, mu1, cv::Size(11, 11), 1.5);
    cv::GaussianBlur(img2, mu2, cv::Size(11, 11), 1.5);
    
    cv::Mat mu1_2 = mu1.mul(mu1);
    cv::Mat mu2_2 = mu2.mul(mu2);
    cv::Mat mu1_mu2 = mu1.mul(mu2);
    
    cv::Mat sigma1_2, sigma2_2, sigma12;
    cv::GaussianBlur(img1.mul(img1), sigma1_2, cv::Size(11, 11), 1.5);
    cv::GaussianBlur(img2.mul(img2), sigma2_2, cv::Size(11, 11), 1.5);
    cv::GaussianBlur(img1.mul(img2), sigma12, cv::Size(11, 11), 1.5);
    
    sigma1_2 -= mu1_2;
    sigma2_2 -= mu2_2;
    sigma12 -= mu1_mu2;
    
    cv::Mat ssim_map = ((2 * mu1_mu2 + C1).mul(2 * sigma12 + C2)) /
                       ((mu1_2 + mu2_2 + C1).mul(sigma1_2 + sigma2_2 + C2));
    
    return static_cast<float>(cv::mean(ssim_map)[0]);
}

VideoProcessor::CompressionParams VideoProcessor::optimizeParameters(const cv::Mat& frame, float target_quality) {
    CompressionParams params;
    
    // Extract features from the frame
    vector<float> features = analyzeFrame(frame);
    
    // Predict quality for different parameter combinations
    float best_quality_diff = std::numeric_limits<float>::max();
    
    // Grid search over parameters
    for (int bitrate : {1000000, 2000000, 4000000, 8000000}) {
        for (float scale : {0.5f, 0.75f, 1.0f}) {
            int width = static_cast<int>(frame.cols * scale);
            int height = static_cast<int>(frame.rows * scale);
            
            // Predict quality for this parameter combination
            float predicted_quality = predictQuality(features);
            float quality_diff = std::abs(predicted_quality - target_quality);
            
            if (quality_diff < best_quality_diff) {
                best_quality_diff = quality_diff;
                params.bitrate = bitrate;
                params.width = width;
                params.height = height;
                params.preset = "medium";
                params.target_quality = predicted_quality;
            }
        }
    }
    
    return params;
}

vector<float> VideoProcessor::extractFeatures(const cv::Mat& frame) {
    vector<float> features;
    features.reserve(128);  // Pre-allocate space for features
    
    // Convert to floating point for statistical features
    cv::Mat float_frame;
    frame.convertTo(float_frame, CV_32F, 1.0/255.0);
    
    // Basic statistical features
    cv::Scalar mean, stddev;
    cv::meanStdDev(float_frame, mean, stddev);
    
    // Add mean and stddev for each channel
    for (int i = 0; i < 3; ++i) {
        features.push_back(static_cast<float>(mean[i]));
        features.push_back(static_cast<float>(stddev[i]));
    }
    
    // Edge detection features (using original 8-bit frame)
    cv::Mat edges;
    cv::Canny(frame, edges, 100, 200);
    features.push_back(static_cast<float>(cv::countNonZero(edges)) / (frame.rows * frame.cols));
    
    // Texture features using GLCM
    cv::Mat gray;
    cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);
    
    // Fill remaining features with placeholder values
    while (features.size() < 128) {
        features.push_back(0.0f);
    }
    
    return features;
}

float VideoProcessor::predictQuality(const vector<float>& features) {
    // Simple weighted sum of features (in practice, this would be a more sophisticated model)
    float quality = 0.0f;
    for (size_t i = 0; i < features.size(); ++i) {
        quality += features[i] * model_weights_[i];
    }
    return std::min(1.0f, std::max(0.0f, quality));
}

} // namespace video_optimizer
