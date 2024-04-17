# # import tkinter as tk
# # import threading
# # import time
# # from pynput import keyboard
# # import pygame

# # class KeyPressRecorder:
# #     def __init__(self):
# #         self.timestamps = []
# #         self.listener = None

# #     def start_recording(self):
# #         self.timestamps = []  # Reset timestamps
# #         self.listener = keyboard.Listener(on_press=self.record_timestamp)
# #         self.listener.start()

# #     def record_timestamp(self, key):
# #         self.timestamps.append(time.time())

# #     # def stop_recording(self):
# #     #     if self.listener:
# #     #         self.listener.stop()

# # class AudioPlayer:
# #     def __init__(self, audio_file):
# #         self.audio_file = audio_file

# #     def play_audio(self):
# #         pygame.mixer.init()
# #         pygame.mixer.music.load(self.audio_file)
# #         pygame.mixer.music.play()

# #     # def stop_audio(self):
# #     #     pygame.mixer.music.stop()

# #     def replay_audio(self):
# #         pygame.mixer.music.rewind()
# #         pygame.mixer.music.play()

# # class GUI:
# #     def __init__(self):
# #         self.root = tk.Tk()
# #         self.root.title("Simple Recorder and Player")

# #         self.recorder = KeyPressRecorder()
# #         self.player = AudioPlayer("Counting stars.wav")

# #         self.start_button = tk.Button(self.root, text="Start", command=self.start_recording_and_playing)
# #         self.start_button.pack()

# #         # self.stop_audio_button = tk.Button(self.root, text="Stop Audio", command=self.stop_audio)
# #         # self.stop_audio_button.pack()

# #         self.replay_button = tk.Button(self.root, text="Replay Audio", command=self.replay_audio)
# #         self.replay_button.pack()

# #         self.timestamps_text = tk.Text(self.root, height=10, width=40)
# #         self.timestamps_text.pack()

# #         self.start_time = None

# #         self.remaining_time_label = tk.Label(self.root, text="Remaining Time: 45 seconds")
# #         self.remaining_time_label.pack()

# #     def start_timer(self):
# #         self.remaining_time = 45  # Set initial remaining time
# #         self.timer_running = True
        
# #         while self.timer_running and self.remaining_time >= 0:
# #             self.remaining_time_label.config(text=f"Remaining Time: {self.remaining_time} seconds")
# #             self.root.update()
# #             time.sleep(1)
# #             self.remaining_time -= 1

# #         self.remaining_time_label.config(text="Time's up!")  # Update label after countdown finishes

# #     def stop_timer(self):
# #         self.timer_running = False

# #     def start_recording_and_playing(self):
# #         self.start_time = time.time()  # Record the start time
# #         self.recording_thread = threading.Thread(target=self.recorder.start_recording)
# #         self.recording_thread.start()

# #         self.playing_thread = threading.Thread(target=self.player.play_audio)
# #         self.playing_thread.start()

# #         self.update_timestamps()

# #         if not self.timer_running:
# #             self.timer_running = True
# #             self.start_timer()


# #     def update_timestamps(self):
# #         while True:
# #             if self.recorder.timestamps:
# #                 elapsed_time = (time.time() - self.start_time)  # Elapsed time in seconds
# #                 timestamp = self.recorder.timestamps.pop(0)
# #                 self.timestamps_text.insert(tk.END, f"{elapsed_time:.3f} s\n")  # Display with 3 decimal places
# #                 self.timestamps_text.see(tk.END)
# #             self.root.update()  # Update the GUI to show changes
# #             time.sleep(0.005)

# #     # def stop_recording(self):
# #     #     self.recorder.stop_recording()
# #     #     self.recording_thread.join()

# #     # def stop_audio(self):
# #     #     self.player.stop_audio()

# #     def replay_audio(self):
# #         self.player.replay_audio()
# #         self.timestamps_text.delete(1.0, tk.END)  # Clear the text display

# #     def run(self):
# #         self.root.mainloop()

# # if __name__ == "__main__":
# #     # Initialize Pygame mixer
# #     pygame.mixer.init()
# #     # Create and run the GUI
# #     gui = GUI()
# #     gui.run()

import tkinter as tk
import threading
import time
from pynput import keyboard
import pygame
from pynput import mouse

class MouseClickRecorder:
    def __init__(self):
        self.timestamps = []
        self.listener = None

    def start_recording(self):
        self.timestamps = []  # Reset timestamps
        self.listener = mouse.Listener(on_click=self.record_timestamp)
        self.listener.start()

    def record_timestamp(self, x, y, button, pressed):
        if pressed:
            self.timestamps.append(time.time())


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

class AudioPlayer:
    def __init__(self, audio_file):
        self.audio_file = audio_file

    def play_audio(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.audio_file)
        pygame.mixer.music.play()

    # def replay_audio(self):
    #     pygame.mixer.music.rewind()
    #     pygame.mixer.music.play()

    # def reset_audio(self):
    #     pygame.mixer.music.stop()

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple Recorder and Player")

        # self.recorder = KeyPressRecorder()
        self.recorder = MouseClickRecorder()  # Change here
        self.player = AudioPlayer("Counting stars.wav")

        self.start_button = tk.Button(self.root, text="Start", command=self.start_recording_and_playing)
        self.start_button.pack()

        # Add a Canvas widget to the GUI
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.pack()

        # Add text to indicate where to tap
        self.canvas.create_text(100, 100, text="Tap Here!", font=("Arial", 22), fill="black")

        # Bind mouse click events to the canvas
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # self.replay_button = tk.Button(self.root, text="Replay Audio", command=self.replay_audio)
        # self.replay_button.pack()

        self.timestamps_text = tk.Text(self.root, height=10, width=40)
        self.timestamps_text.pack()

        # Bind <Return> key to start_recording_and_playing method
        self.root.bind("<Return>", lambda event: self.start_recording_and_playing())

        self.start_time = None

        self.remaining_time_label = tk.Label(self.root, text="Remaining Time: 75 seconds")
        self.remaining_time_label.pack()

        self.timer_running = False

        self.participant = "Ujjwal"
        self.songID = "A"

    def start_timer(self):
        self.remaining_time = 75  # Set initial remaining time
        self.update_remaining_time()

    def update_remaining_time(self):
        if self.timer_running and self.remaining_time >= 0:
            self.remaining_time_label.config(text=f"Remaining Time: {self.remaining_time} seconds")
            self.remaining_time -= 1
            self.root.after(1000, self.update_remaining_time)
        else:
            self.remaining_time_label.config(text="Time's up!")
            self.save_timestamps_to_file()

    def start_recording_and_playing(self):
        self.start_time = time.time()  # Record the start time
        self.recording_thread = threading.Thread(target=self.recorder.start_recording)
        self.recording_thread.start()

        self.playing_thread = threading.Thread(target=self.player.play_audio)
        self.playing_thread.start()

        self.update_timestamps()

        if not self.timer_running:
            self.timer_running = True
            self.start_timer()

    def update_timestamps(self):
        if self.recorder.timestamps:
            elapsed_time = (time.time() - self.start_time)  # Elapsed time in seconds
            timestamp = self.recorder.timestamps.pop(0)
            self.timestamps_text.insert(tk.END, f"{elapsed_time:.3f} s\n")  # Display with 3 decimal places
            self.timestamps_text.see(tk.END)
        self.root.after(5, self.update_timestamps)  # Schedule the method to run again after 5 milliseconds

    def on_canvas_click(self, event):
        # This function will be called when the canvas is clicked
        # You can handle tap events here
        # x = self.canvas.canvasx(event.x)
        # y = self.canvas.canvasy(event.y)
        # timestamp = time.time()
        # self.timestamps_text.insert(tk.END, f"{timestamp:.3f} s\n")
        # self.timestamps_text.see(tk.END)
        self.update_timestamps()
    
    # def replay_audio(self):
    #     self.player.replay_audio()
    #     self.timestamps_text.delete(1.0, tk.END)  # Clear the text display
    #     self.timer_running = False
    #     self.start_timer()

    def save_timestamps_to_file(self):
        with open(f"timestamps_{self.participant}_{self.songID}.txt", "w") as file:
            file.write(self.timestamps_text.get("1.0", tk.END))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Initialize Pygame mixer
    pygame.mixer.init()
    # Create and run the GUI
    gui = GUI()
    gui.run()
