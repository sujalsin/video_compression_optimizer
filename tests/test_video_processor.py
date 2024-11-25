import sys
import os
import cv2
import numpy as np

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from cpp_src.build.video_processor import VideoProcessor
    print("Successfully imported VideoProcessor module")
    
    # Create an instance of VideoProcessor
    processor = VideoProcessor()
    print("Successfully created VideoProcessor instance")
    
    # Create a test frame
    test_frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
    # Add some patterns to the frame for better testing
    cv2.rectangle(test_frame, (100, 100), (500, 500), (255, 255, 255), -1)
    cv2.circle(test_frame, (1000, 500), 200, (0, 255, 0), -1)
    
    print("Testing frame analysis...")
    features = processor.analyze_frame(test_frame)
    print(f"Frame analysis features: {features}")
    
    # Test PSNR calculation
    print("\nTesting PSNR calculation...")
    compressed_frame = cv2.GaussianBlur(test_frame, (7, 7), 0)  # Simulate compression
    psnr = processor.calculate_psnr(test_frame, compressed_frame)
    print(f"PSNR value: {psnr}")
    
    # Test SSIM calculation
    print("\nTesting SSIM calculation...")
    ssim = processor.calculate_ssim(test_frame, compressed_frame)
    print(f"SSIM value: {ssim}")
    
    # Test compression parameter optimization
    print("\nTesting compression parameter optimization...")
    params = processor.optimize_parameters(test_frame, 0.9)  # target quality of 0.9
    print(f"Optimized parameters: {params}")
    
except ImportError as e:
    print(f"Error importing module: {e}")
except Exception as e:
    print(f"Error during testing: {e}")
    import traceback
    traceback.print_exc()
