import ffmpeg
import numpy as np
from pathlib import Path
import os
from quality_assessment import QualityAssessor

class VideoCompressor:
    def __init__(self):
        self.quality_assessor = QualityAssessor()
        self.preset_settings = {
            'low': {'crf': 28, 'preset': 'veryfast'},
            'medium': {'crf': 23, 'preset': 'medium'},
            'high': {'crf': 18, 'preset': 'slow'},
        }

    def _get_video_info(self, input_path):
        """Get video metadata using ffmpeg."""
        probe = ffmpeg.probe(input_path)
        video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        return video_info

    def _get_output_resolution(self, original_width, original_height, target_res):
        """Calculate output resolution maintaining aspect ratio."""
        if target_res == 'original':
            return original_width, original_height
        
        height_map = {'1080p': 1080, '720p': 720, '480p': 480}
        target_height = height_map.get(target_res)
        if not target_height:
            return original_width, original_height
        
        aspect_ratio = original_width / original_height
        target_width = int(target_height * aspect_ratio)
        return target_width, target_height

    def compress_video(self, input_path, settings, progress_callback=None):
        """Compress video with the specified settings."""
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input video not found: {input_path}")

        # Get video info
        video_info = self._get_video_info(input_path)
        original_width = int(video_info['width'])
        original_height = int(video_info['height'])

        # Prepare output path
        input_path = Path(input_path)
        output_path = input_path.parent / f"{input_path.stem}_compressed{input_path.suffix}"

        # Get compression settings
        preset = settings['preset']
        target_bitrate = settings['bitrate']
        output_width, output_height = self._get_output_resolution(
            original_width, original_height, settings['resolution']
        )

        # Build ffmpeg command
        stream = ffmpeg.input(str(input_path))
        
        # Apply compression settings
        if preset in self.preset_settings:
            compression_settings = self.preset_settings[preset]
        else:  # Custom settings
            compression_settings = {
                'crf': 23,  # Default CRF value
                'preset': 'medium'
            }

        # Build output stream with settings
        stream = ffmpeg.output(
            stream,
            str(output_path),
            vcodec='libx264',
            acodec='aac',
            video_bitrate=f"{target_bitrate}M",
            s=f"{output_width}x{output_height}",
            crf=compression_settings['crf'],
            preset=compression_settings['preset']
        )

        # Run compression
        try:
            process = ffmpeg.run_async(
                stream,
                pipe_stdout=True,
                pipe_stderr=True
            )
            
            # Monitor progress
            if progress_callback:
                while True:
                    if process.poll() is not None:
                        break
                    # Estimate progress (this is a simplified version)
                    progress_callback(50)  # You would need to implement proper progress tracking
            
            process.wait()

            # Assess quality
            quality_score = self.quality_assessor.assess_quality(str(output_path))
            
            if progress_callback:
                progress_callback(100)

            return {
                'output_path': str(output_path),
                'quality_score': quality_score,
                'compression_ratio': os.path.getsize(output_path) / os.path.getsize(input_path)
            }

        except ffmpeg.Error as e:
            raise RuntimeError(f"FFmpeg error: {e.stderr.decode()}")
        except Exception as e:
            raise RuntimeError(f"Compression error: {str(e)}")
