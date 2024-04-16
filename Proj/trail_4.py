from moviepy.editor import VideoClip
import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up screen dimensions
width, height = 800, 600
duration = 45  # in seconds
bpm = 140  # beats per minute

# Convert BPM to FPS
fps = bpm / 60

# Set up colors
BLACK = (0, 0, 0)
colors = [(102, 178, 255), (152, 255, 178), (204, 153, 255), (255, 204, 153), (255, 255, 153)]

# Set up circles
num_circles = 10
circle_radius = 30
circle_positions = []
for i in range(num_circles):
    angle = (2 * math.pi / num_circles) * i
    x = width // 2 + int(200 * math.cos(angle))
    y = height // 2 + int(200 * math.sin(angle))
    circle_positions.append((x, y))

# Define function to draw a frame
def make_frame(t):
    surface = pygame.Surface((width, height))
    surface.fill(BLACK)

    # Calculate the current color index for each circle
    current_colors = []
    for i in range(num_circles):
        beat_index = int(t * (bpm / 60))
        color_index = (beat_index + i) % len(colors)
        current_colors.append(colors[color_index])

    # Draw circles
    for i, (x, y) in enumerate(circle_positions):
        color = current_colors[i]
        pygame.draw.circle(surface, color, (x, y), circle_radius)

    return pygame.surfarray.array3d(surface)

# Create VideoClip
clip = VideoClip(make_frame, duration=duration)

# Export as video file
clip.write_videofile("rhythmic_visuals_140_bpm.mp4", fps=fps)
