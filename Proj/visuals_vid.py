import pygame
import sys
import math
from moviepy.editor import ImageSequenceClip

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rhythmic Visuals")

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

# Set up timing
beat_frequency = 2  # Beats per second
beat_interval = 1000 // beat_frequency  # Convert frequency to milliseconds
last_beat_time = pygame.time.get_ticks()

# List to store frames
frames = []

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check if it's time for a beat
    current_time = pygame.time.get_ticks()
    if current_time - last_beat_time >= beat_interval:
        # Change colors of circles
        colors.insert(0, colors.pop())
        last_beat_time = current_time

    # Clear the screen
    screen.fill(BLACK)

    # Draw circles
    for i, (x, y) in enumerate(circle_positions):
        color = colors[i % len(colors)]
        pygame.draw.circle(screen, color, (x, y), circle_radius)

    # Update the display
    pygame.display.flip()

    # Capture frame
    pygame.image.save(screen, f"frame{len(frames):05}.png")
    frames.append(f"frame{len(frames):05}.png")

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Convert frames to video using MoviePy
clip = ImageSequenceClip(frames, fps=30)
clip.write_videofile("output_video.mp4", codec="libx264")

# Quit Pygame
pygame.quit()
sys.exit()
