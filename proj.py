# import tkinter as tk
# import threading
# import time
# import pygame
# from pynput import keyboard

# class KeyPressRecorder:
#     def __init__(self):
#         self.timestamps = []
#         self.listener = None

#     def start_recording(self):
#         self.listener = keyboard.Listener(on_press=self.record_timestamp)
#         self.listener.start()

#     def record_timestamp(self, key):
#         self.timestamps.append(time.time())

#     def stop_recording(self):
#         if self.listener:
#             self.listener.stop()

# class AudioPlayer:
#     def __init__(self, audio_file):
#         self.audio_file = audio_file

#     def play_audio(self):
#         pygame.mixer.init()
#         pygame.mixer.music.load(self.audio_file)
#         pygame.mixer.music.play()

# class GUI:
#     def __init__(self):
#         self.root = tk.Tk()
#         self.root.title("Simple Recorder and Player")

#         self.recorder = KeyPressRecorder()
#         self.player = AudioPlayer("/home/anika/Desktop/MMT/file_example_MP3_700KB.mp3")

#         self.start_button = tk.Button(self.root, text="Start", command=self.start_recording_and_playing)
#         self.start_button.pack()

#         self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_recording)
#         self.stop_button.pack()

#     def start_recording_and_playing(self):
#         self.recording_thread = threading.Thread(target=self.recorder.start_recording)
#         self.recording_thread.start()

#         self.playing_thread = threading.Thread(target=self.player.play_audio)
#         self.playing_thread.start()

#     def stop_recording(self):
#         self.recorder.stop_recording()
#         self.recording_thread.join()

#     def run(self):
#         self.root.mainloop()

# if __name__ == "__main__":
#     # Initialize Pygame mixer
#     pygame.mixer.init()
#     # Create and run the GUI
#     gui = GUI()
#     gui.run()


# Displaying absolute time right now


# import tkinter as tk
# import threading
# import time
# from pynput import keyboard
# import pygame

# class KeyPressRecorder:
#     def __init__(self):
#         self.timestamps = []
#         self.listener = None

#     def start_recording(self):
#         self.listener = keyboard.Listener(on_press=self.record_timestamp)
#         self.listener.start()

#     def record_timestamp(self, key):
#         self.timestamps.append(time.time())

#     def stop_recording(self):
#         if self.listener:
#             self.listener.stop()

# class AudioPlayer:
#     def __init__(self, audio_file):
#         self.audio_file = audio_file

#     def play_audio(self):
#         pygame.mixer.init()
#         pygame.mixer.music.load(self.audio_file)
#         pygame.mixer.music.play()

# class GUI:
#     def __init__(self):
#         self.root = tk.Tk()
#         self.root.title("Simple Recorder and Player")

#         self.recorder = KeyPressRecorder()
#         self.player = AudioPlayer("file_example_MP3_700KB.mp3")

#         self.start_button = tk.Button(self.root, text="Start", command=self.start_recording_and_playing)
#         self.start_button.pack()

#         self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_recording)
#         self.stop_button.pack()

#         self.timestamps_text = tk.Text(self.root, height=10, width=40)
#         self.timestamps_text.pack()

#     def start_recording_and_playing(self):
#         self.recording_thread = threading.Thread(target=self.recorder.start_recording)
#         self.recording_thread.start()

#         self.playing_thread = threading.Thread(target=self.player.play_audio)
#         self.playing_thread.start()

#         self.update_timestamps()

#     # def update_timestamps(self):
#     #     while True:
#     #         if self.recorder.timestamps:
#     #             timestamp = self.recorder.timestamps.pop(0)
#     #             self.timestamps_text.insert(tk.END, f"{time.strftime('%H:%M:%S', time.localtime(timestamp))}\n")
#     #             self.timestamps_text.see(tk.END)
#     #         time.sleep(0.1)

#     def update_timestamps(self):
#         while True:
#             if self.recorder.timestamps:
#                 timestamp = self.recorder.timestamps.pop(0)
#                 self.timestamps_text.insert(tk.END, f"{time.strftime('%H:%M:%S', time.localtime(timestamp))}\n")
#                 self.timestamps_text.see(tk.END)
#             self.root.update()  # Update the GUI to show changes
#             time.sleep(0.1)

#     def stop_recording(self):
#         self.recorder.stop_recording()
#         self.recording_thread.join()

#     def run(self):
#         self.root.mainloop()

# if __name__ == "__main__":
#     # Initialize Pygame mixer
#     pygame.mixer.init()
#     # Create and run the GUI
#     gui = GUI()
#     gui.run()

# displaying relative time down to milliseconds

import tkinter as tk
import threading
import time
from pynput import keyboard
import pygame

class KeyPressRecorder:
    def __init__(self):
        self.timestamps = []
        self.listener = None

    def start_recording(self):
        self.timestamps = []  # Reset timestamps
        self.listener = keyboard.Listener(on_press=self.record_timestamp)
        self.listener.start()

    def record_timestamp(self, key):
        self.timestamps.append(time.time())

    def stop_recording(self):
        if self.listener:
            self.listener.stop()

class AudioPlayer:
    def __init__(self, audio_file):
        self.audio_file = audio_file

    def play_audio(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.audio_file)
        pygame.mixer.music.play()

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple Recorder and Player")

        self.recorder = KeyPressRecorder()
        self.player = AudioPlayer("Counting stars.wav")

        self.start_button = tk.Button(self.root, text="Start", command=self.start_recording_and_playing)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_recording)
        self.stop_button.pack()

        self.timestamps_text = tk.Text(self.root, height=10, width=40)
        self.timestamps_text.pack()

        self.start_time = None

    def start_recording_and_playing(self):
        self.start_time = time.time()  # Record the start time
        self.recording_thread = threading.Thread(target=self.recorder.start_recording)
        self.recording_thread.start()

        self.playing_thread = threading.Thread(target=self.player.play_audio)
        self.playing_thread.start()

        self.update_timestamps()

    def update_timestamps(self):
        while True:
            if self.recorder.timestamps:
                elapsed_time = (time.time() - self.start_time)  # Elapsed time in seconds
                timestamp = self.recorder.timestamps.pop(0)
                self.timestamps_text.insert(tk.END, f"{elapsed_time:.3f} s\n")  # Display with 3 decimal places
                self.timestamps_text.see(tk.END)
            self.root.update()  # Update the GUI to show changes
            time.sleep(0.005)

    def stop_recording(self):
        self.recorder.stop_recording()
        self.recording_thread.join()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Initialize Pygame mixer
    pygame.mixer.init()
    # Create and run the GUI
    gui = GUI()
    gui.run()

# trying to write the output to a file

# import tkinter as tk
# import threading
# import time
# from pynput import keyboard
# import pygame

# class KeyPressRecorder:
#     def __init__(self):
#         self.timestamps = []
#         self.listener = None

#     def start_recording(self):
#         self.timestamps = []  # Reset timestamps
#         self.listener = keyboard.Listener(on_press=self.record_timestamp)
#         self.listener.start()

#     def record_timestamp(self, key):
#         self.timestamps.append(time.time())

#     def stop_recording(self):
#         if self.listener:
#             self.listener.stop()

# class AudioPlayer:
#     def __init__(self, audio_file):
#         self.audio_file = audio_file

#     def play_audio(self):
#         pygame.mixer.init()
#         pygame.mixer.music.load(self.audio_file)
#         pygame.mixer.music.play()

# class TimestampWriter:
#     def __init__(self, file_path):
#         self.file_path = file_path

#     def write_timestamps(self, timestamps):
#         with open(self.file_path, 'w') as file:
#             for timestamp in timestamps:
#                 file.write(f"{timestamp}\n")

# class GUI:
#     def __init__(self):
#         self.root = tk.Tk()
#         self.root.title("Simple Recorder and Player")

#         self.recorder = KeyPressRecorder()
#         self.player = AudioPlayer("your_audio_file.mp3")
#         self.timestamp_writer = TimestampWriter("timestamps.txt")

#         self.start_button = tk.Button(self.root, text="Start", command=self.start_recording_and_playing)
#         self.start_button.pack()

#         self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_recording)
#         self.stop_button.pack()

#     def start_recording_and_playing(self):
#         self.recording_thread = threading.Thread(target=self.record_and_play)
#         self.recording_thread.start()

#     def record_and_play(self):
#         self.recorder.start_recording()
#         self.player.play_audio()
#         self.recorder.stop_recording()
#         self.timestamp_writer.write_timestamps(self.recorder.timestamps)

#     def stop_recording(self):
#         pass  # Do nothing for now

#     def run(self):
#         self.root.mainloop()

# if __name__ == "__main__":
#     # Initialize Pygame mixer
#     pygame.mixer.init()
#     # Create and run the GUI
#     gui = GUI()
#     gui.run()

