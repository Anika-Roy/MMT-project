import tkinter as tk
import threading
import time
from pynput import mouse
import pygame
from moviepy.editor import VideoFileClip

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


class VideoPlayer:
    def __init__(self, video_file):
        self.video_file = video_file

    def play_video(self):
        video = VideoFileClip(self.video_file)
        video.preview()
        video.close()


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple Recorder and Player")

        self.recorder = MouseClickRecorder()
        self.player = VideoPlayer("../vis_dist_files/C.mp4")  # Change path to your video file

        self.start_button = tk.Button(self.root, text="Start", command=self.start_recording_and_playing)
        self.start_button.pack()

        self.canvas = tk.Canvas(self.root, width=300, height=400, bg="white")
        self.canvas.pack()

        self.canvas.create_text(100, 100, text="Tap Here!", font=("Arial", 22), fill="black")

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.timestamps_text = tk.Text(self.root, height=10, width=30)
        self.timestamps_text.pack()

        self.root.bind("<Return>", lambda event: self.start_recording_and_playing())

        self.start_time = None

        self.remaining_time_label = tk.Label(self.root, text="Remaining Time: 45 seconds")
        self.remaining_time_label.pack()

        self.timer_running = False

        self.participant = "Ujjwal"
        self.songID = "C"

    # def run(self):
    #     self.root.geometry("+0+0")  # Set window position to top-left corner
    #     self.root.mainloop()

    # def run(self):
    #     # Set window attributes to position at the top-left corner
    #     self.root.attributes("-topmost", True)
    #     self.root.attributes("-alpha", 0.0)  # Optional: make the window transparent initially
    #     self.root.attributes("-fullscreen", False)
    #     self.root.attributes("-zoomed", False)
    #     self.root.update_idletasks()  # Ensure changes take effect
    #     self.root.attributes("-alpha", 1.0)  # Optional: restore window transparency
    #     self.root.geometry("+0+0")  # Set window position to top-left corner
    #     self.root.mainloop()

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

    def start_recording_and_playing(self):
        self.start_time = time.time()  # Record the start time
        self.recording_thread = threading.Thread(target=self.recorder.start_recording)
        self.recording_thread.start()

        self.playing_thread = threading.Thread(target=self.player.play_video)
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
        self.update_timestamps()

    def save_timestamps_to_file(self):
        with open(f"../vis_dist_timestamps/vis_timestamps_{self.participant}_{self.songID}.txt", "w") as file:
            file.write(self.timestamps_text.get("1.0", tk.END))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Initialize Pygame mixer
    pygame.mixer.init()
    # Create and run the GUI
    gui = GUI()
    gui.run()
