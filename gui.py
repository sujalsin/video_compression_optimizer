import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from pathlib import Path

class VideoCompressorGUI:
    def __init__(self, compressor, quality_assessor):
        # Create the root window
        self.root = tk.Tk()
        self.root.title('Intelligent Video Compression Optimizer')
        self.root.geometry('800x600')
        
        # Store references to components
        self.compressor = compressor
        self.quality_assessor = quality_assessor
        self.video_path = None
        
        # Initialize GUI components
        self._init_gui()
        
        # Configure window close handler
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
    def _init_gui(self):
        """Initialize all GUI components"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="Video Selection", padding="5")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.file_label = ttk.Label(file_frame, text='No file selected')
        self.file_label.pack(side=tk.LEFT, expand=True, padx=5)
        
        select_button = ttk.Button(file_frame, text='Select Video', command=self._select_file)
        select_button.pack(side=tk.RIGHT, padx=5)
        
        # Settings
        settings_frame = ttk.LabelFrame(main_frame, text="Compression Settings", padding="5")
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Quality preset
        preset_frame = ttk.Frame(settings_frame)
        preset_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(preset_frame, text='Quality Preset:').pack(side=tk.LEFT, padx=5)
        self.preset_var = tk.StringVar(value='Medium')
        preset_combo = ttk.Combobox(preset_frame, textvariable=self.preset_var, state='readonly')
        preset_combo['values'] = ('Low', 'Medium', 'High', 'Custom')
        preset_combo.pack(side=tk.LEFT, padx=5)
        
        # Bitrate
        bitrate_frame = ttk.Frame(settings_frame)
        bitrate_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(bitrate_frame, text='Target Bitrate (Mbps):').pack(side=tk.LEFT, padx=5)
        self.bitrate_var = tk.DoubleVar(value=5.0)
        bitrate_spin = ttk.Spinbox(bitrate_frame, from_=0.1, to=50.0, increment=0.1,
                                textvariable=self.bitrate_var, width=10)
        bitrate_spin.pack(side=tk.LEFT, padx=5)
        
        # Resolution
        resolution_frame = ttk.Frame(settings_frame)
        resolution_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(resolution_frame, text='Output Resolution:').pack(side=tk.LEFT, padx=5)
        self.resolution_var = tk.StringVar(value='Original')
        resolution_combo = ttk.Combobox(resolution_frame, textvariable=self.resolution_var, state='readonly')
        resolution_combo['values'] = ('Original', '1080p', '720p', '480p')
        resolution_combo.pack(side=tk.LEFT, padx=5)
        
        # Progress
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                         maximum=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        self.start_button = ttk.Button(button_frame, text='Start Compression',
                                    command=self._start_compression)
        self.start_button.pack(pady=5)
        self.start_button['state'] = 'disabled'
        
        # Status
        self.status_label = ttk.Label(main_frame, text='Ready')
        self.status_label.pack(pady=5)
    
    def _select_file(self):
        """Handle file selection"""
        filetypes = (
            ('Video files', '*.mp4 *.avi *.mkv *.mov'),
            ('All files', '*.*')
        )
        
        filename = filedialog.askopenfilename(
            title='Select a video file',
            filetypes=filetypes
        )
        
        if filename:
            self.video_path = filename
            self.file_label['text'] = Path(filename).name
            self.start_button['state'] = 'normal'
            self.status_label['text'] = 'Ready to compress'
    
    def _update_progress(self, value):
        """Update progress bar"""
        self.progress_var.set(value)
        self.root.update_idletasks()
    
    def _start_compression(self):
        """Handle compression start"""
        if not self.video_path:
            messagebox.showerror('Error', 'Please select a video file first')
            return
        
        settings = {
            'preset': self.preset_var.get().lower(),
            'bitrate': self.bitrate_var.get(),
            'resolution': self.resolution_var.get()
        }
        
        self.start_button['state'] = 'disabled'
        self.progress_var.set(0)
        self.status_label['text'] = 'Compressing...'
        
        # Run compression in a separate thread
        def compression_thread():
            try:
                result = self.compressor.compress_video(
                    self.video_path,
                    settings,
                    progress_callback=self._update_progress
                )
                self.root.after(0, self._compression_finished, result)
            except Exception as e:
                self.root.after(0, self._compression_error, str(e))
        
        threading.Thread(target=compression_thread, daemon=True).start()
    
    def _compression_finished(self, result):
        """Handle compression completion"""
        self.status_label['text'] = (
            f'Compression completed!\n'
            f'Output: {Path(result["output_path"]).name}\n'
            f'Quality Score: {result["quality_score"]:.2f}\n'
            f'Compression Ratio: {result["compression_ratio"]:.2f}x'
        )
        self.start_button['state'] = 'normal'
    
    def _compression_error(self, error_msg):
        """Handle compression error"""
        messagebox.showerror('Error', f'Compression failed: {error_msg}')
        self.status_label['text'] = 'Error occurred during compression'
        self.start_button['state'] = 'normal'
    
    def _on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.quit()
            self.root.destroy()
    
    def run(self):
        """Start the GUI main loop"""
        try:
            # Center the window on screen
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            self.root.geometry(f'{width}x{height}+{x}+{y}')
            
            # Start main loop
            self.root.mainloop()
        except Exception as e:
            print(f"Error in GUI main loop: {str(e)}")
            raise
