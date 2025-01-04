# CodeClauseInternship_Simple-Voice-Recorder
To develop a simple voice recording application in Python, we will utilize libraries such as **pyaudio** for audio recording and **tkinter** for the graphical user interface (GUI). Here’s a step-by-step guide on how you can build this application:

### Steps to Build the Application:

1. *Install Required Libraries:*
   - You need to install the pyaudio library for audio recording and tkinter for the GUI.
   - You can install pyaudio using pip (if it's not installed already):
   
   bash
   pip install pyaudio
   

   tkinter comes pre-installed with Python in most distributions.

2. *Create the GUI using Tkinter:*
   The GUI will have buttons for:
   - *Start Recording*: To start the recording process.
   - *Stop Recording*: To stop the recording process.
   - *Save Recording*: To save the recorded audio to a file.

3. *Handle Audio Recording with PyAudio:*
   Use *PyAudio* to capture audio from the microphone and save it as a .wav file.

4. *Integrate the functionality in the GUI:*
   Use the tkinter buttons to trigger audio recording actions.

### Full Python Code for the Voice Recording Application:

python
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


### How It Works:

1. *Tkinter GUI:*
   - *Start Recording Button*: Starts the audio recording.
   - *Stop Recording Button*: Stops the audio recording and enables the Save button.
   - *Save Recording Button*: Saves the recorded audio to a file (.wav format).

2. *PyAudio for Audio Recording:*
   - The program uses the pyaudio.PyAudio class to open a stream to record audio from the microphone.
   - Audio is captured in chunks of data (1024 frames per buffer).
   - The audio is stored in self.frames and written to a .wav file once the recording is stopped.

3. *Multithreading:*
   - Audio recording is handled in a separate thread (record_thread) to prevent the GUI from freezing during recording.
   
4. *Saving the Audio:*
   - When you press the "Save Recording" button, the audio is saved to a file with the name recording.wav. If that file already exists, it will save it as recording_1.wav, and so on.

### How to Run:

1. Save the code to a Python file (e.g., voice_recorder.py).
2. Run the script using Python:
   
   bash
   python voice_recorder.py
   

3. A window will appear with buttons to *Start Recording, **Stop Recording, and **Save Recording*.

### Enhancements You Could Add:

- *Pause and Resume Recording*: Add buttons to pause and resume the recording.
- *Timer*: Display a timer to show how long the recording has been going on.
- *Error Handling*: Add error handling for situations where the microphone is not available or there’s a failure in saving the file.
- *File Naming*: Allow the user to input a custom filename for the saved recording.

This provides a simple, user-friendly voice recorder application. Let me know if you need any further customizations!
