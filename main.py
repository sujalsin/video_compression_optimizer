#!/usr/bin/env python3

import sys
import traceback
from gui import VideoCompressorGUI
from compression import VideoCompressor
from quality_assessment import QualityAssessor

def main():
    """Main entry point of the application."""
    try:
        # Initialize core components
        print("Initializing components...")
        compressor = VideoCompressor()
        quality_assessor = QualityAssessor()
        
        print("Creating GUI...")
        # Create and run the GUI
        app = VideoCompressorGUI(compressor, quality_assessor)
        print("Starting GUI main loop...")
        app.run()
    except Exception as e:
        print(f"Error starting application: {str(e)}")
        print("Traceback:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
