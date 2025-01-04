import tkinter as tk
import pyaudio
import wave
import threading
import os

class VoiceRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Recorder")
        self.root.geometry("300x200")
        
        self.recording = False
        self.frames = []
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.channels = 1  # mono sound
        self.rate = 44100  # sample rate (samples per second)
        self.chunk = 1024  # number of frames per buffer
        
        # PyAudio instance
        self.p = pyaudio.PyAudio()
        
        # Create buttons
        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=20)

        self.stop_button = tk.Button(root, text="Stop Recording", state=tk.DISABLED, command=self.stop_recording)
        self.stop_button.pack(pady=20)

        self.save_button = tk.Button(root, text="Save Recording", state=tk.DISABLED, command=self.save_recording)
        self.save_button.pack(pady=20)

    def start_recording(self):
        """Start recording the audio"""
        self.recording = True
        self.frames = []  # Clear previous frames
        self.stop_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.DISABLED)

        # Open stream
        self.stream = self.p.open(format=self.sample_format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunk)

        # Start a thread to record audio
        self.record_thread = threading.Thread(target=self.record_audio)
        self.record_thread.start()

    def record_audio(self):
        """Record audio and store in frames"""
        while self.recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
        
        self.stream.stop_stream()
        self.stream.close()

    def stop_recording(self):
        """Stop recording audio"""
        self.recording = False
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)

    def save_recording(self):
        """Save the recorded audio to a file"""
        filename = "recording.wav"
        if os.path.exists(filename):
            filename = "recording_1.wav"
        
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.sample_format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
        
        print(f"Recording saved as {filename}")
        
        # Reset buttons
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceRecorder(root)
    root.mainloop()
