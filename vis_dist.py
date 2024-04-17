import tkinter as tk
import threading
import time
from pynput import keyboard
import pygame
from pynput import mouse
from moviepy.editor import VideoFileClip
import imageio
from PIL import Image, ImageTk

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

# class VideoPlayer:
#     def __init__(self, video_file):
#         self.video_file = video_file
#         self.clip = VideoFileClip(video_file)
#         self.frames_iterator = self.clip.iter_frames()
#         self.audio = self.clip.audio  # Get the audio from the video

#     def get_next_frame(self):
#         try:
#             frame = next(self.frames_iterator)
#             return ImageTk.PhotoImage(image=Image.fromarray(frame))
#         except StopIteration:
#             return None

#     def play_audio(self):
#         self.audio.preview()  # Play the audio
class VideoPlayer:
    def __init__(self, video_file):
        self.video_file = video_file
        self.clip = VideoFileClip(video_file)
        self.frames_iterator = self.clip.iter_frames()
        self.audio = self.clip.audio  # Get the audio from the video

    def get_next_frame(self):
        try:
            frame = next(self.frames_iterator)
            return ImageTk.PhotoImage(image=Image.fromarray(frame))
        except StopIteration:
            return None

    def play_audio(self):
        self.audio_thread = threading.Thread(target=self._play_audio)
        self.audio_thread.start()

    def _play_audio(self):
        try:
            self.audio.preview()
        except Exception as e:
            print("Error playing audio:", e)


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple Recorder and Player")

        self.recorder = MouseClickRecorder()  # Change here
        self.player = VideoPlayer("distraction_100_100.mp4")  # Change to your video file

        self.start_button = tk.Button(self.root, text="Start", command=self.start_recording_and_playing)
        self.start_button.pack()

        # Bind <Return> key to start_recording_and_playing method
        self.root.bind("<Return>", lambda event: self.start_recording_and_playing())

        # Add a Canvas widget to the GUI for video display
        self.canvas = tk.Canvas(self.root, width=700, height=900, bg="black")
        self.canvas.pack()

        self.timestamps_text = tk.Text(self.root, height=10, width=40)
        self.timestamps_text.pack()

        self.start_time = None

        self.remaining_time_label = tk.Label(self.root, text="Remaining Time: 45 seconds")
        self.remaining_time_label.pack()

        self.timer_running = False

        self.participant = "Ujjwal"
        self.songID = "A"

    def start_timer(self):
        self.remaining_time = 45  # Set initial remaining time
        self.update_remaining_time()

    def update_remaining_time(self):
        if self.timer_running and self.remaining_time >= 0:
            self.remaining_time_label.config(text=f"Remaining Time: {self.remaining_time} seconds")
            self.remaining_time -= 1
            self.root.after(1000, self.update_remaining_time)
        else:
            self.remaining_time_label.config(text="Time's up!")
            self.save_timestamps_to_file()

    # def start_recording_and_playing(self):
    #     self.start_time = time.time()  # Record the start time
    #     self.recording_thread = threading.Thread(target=self.recorder.start_recording)
    #     self.recording_thread.start()

    #     self.update_timestamps()

    #     if not self.timer_running:
    #         self.timer_running = True
    #         self.start_timer()

    #     self.play_video()

    def update_timestamps(self):
        if self.recorder.timestamps:
            elapsed_time = (time.time() - self.start_time)  # Elapsed time in seconds
            timestamp = self.recorder.timestamps.pop(0)
            self.timestamps_text.insert(tk.END, f"{elapsed_time:.3f} s\n")  # Display with 3 decimal places
            self.timestamps_text.see(tk.END)
        self.root.after(5, self.update_timestamps)  # Schedule the method to run again after 5 milliseconds

    # def play_video(self):
    #     frame = self.player.get_next_frame()
    #     if frame:
    #         self.canvas.image = frame  # Keep a reference to prevent garbage collection
    #         self.canvas.create_image(0, 0, anchor=tk.NW, image=frame)
    #         self.root.after(33, self.play_video)  # Schedule the next frame after 33 milliseconds (30 fps)
    #         self.player.play_audio()  # Play the audio
    def play_video(self):
        frame = self.player.get_next_frame()
        if frame:
            self.canvas.delete("all")  # Clear previous frame
            self.canvas.image = frame  # Keep a reference to prevent garbage collection
            self.canvas.create_image(0, 0, anchor=tk.NW, image=frame)
        self.root.after(33, self.play_video)  # Schedule the next frame after 33 milliseconds (30 fps)

    def start_playing_video_thread(self):
        video_thread = threading.Thread(target=self.play_video)
        video_thread.start()

    # def start_recording_and_playing(self):
    #     self.start_time = time.time()  # Record the start time
    #     self.recording_thread = threading.Thread(target=self.recorder.start_recording)
    #     self.recording_thread.start()

    #     self.update_timestamps()

    #     if not self.timer_running:
    #         self.timer_running = True
    #         self.start_timer()

    #     self.start_playing_video_thread()  # Start playing video in a separate thread
    def start_recording_and_playing(self):
        self.start_time = time.time()  # Record the start time
        self.recording_thread = threading.Thread(target=self.recorder.start_recording)
        self.recording_thread.start()

        self.update_timestamps()

        if not self.timer_running:
            self.timer_running = True
            self.start_timer()

        self.start_playing_video_thread()  # Start playing video in a separate thread
        self.player.play_audio()  # Start audio playback


    def save_timestamps_to_file(self):
        with open(f"timestamps_{self.participant}_{self.songID}.txt", "w") as file:
            file.write(self.timestamps_text.get("1.0", tk.END))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Create and run the GUI
    gui = GUI()
    gui.run()
