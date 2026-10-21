import sys
import os  # Added to handle file path operations safely
import math
import pygame

# ----------------------------------------------------
# SETUP
# ----------------------------------------------------
pygame.init()
pygame.mixer.init()

# Window Setup
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SirenSense DEMO1")
clock = pygame.time.Clock()

# Center position of the window
center_x, center_y = WIDTH // 2, HEIGHT // 2

# Detection configurations
RADAR_RADIUS = 300

# State management
state = {
    "active": False,
    "angle": 0.0,
    "distance": 0.0
}
sweep_angle_deg = 0.0
blink_timer = 0

# Interactive practice elements (Fake Ambulance)
ambulance_x = center_x + 150
ambulance_y = center_y - 150
ambulance_speed = 5

# Define the subfolder name where your audio is housed
AUDIO_FOLDER = "audio"
audio_file_name = "Caution_voice.mp3"

# Combine the directory name and file name into a clean path (audio/Caution_voice.mp3)
full_audio_path = os.path.join(AUDIO_FOLDER, audio_file_name)

# Load sound clip with fallback handling targeting the subfolder
try:
    alert_sound = pygame.mixer.Sound(full_audio_path)
except FileNotFoundError:
    alert_sound = None
    print(f"Warning: '{full_audio_path}' not found. Will use console alert for audio event.")

# Font for text display
font = pygame.font.SysFont(None, 48)

# ----------------------------------------------------
# MAIN GAME LOOP
# ----------------------------------------------------
running = True
while running:
    # 1. HANDLE INPUT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move fake ambulance with arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ambulance_x -= ambulance_speed
    if keys[pygame.K_RIGHT]:
        ambulance_x += ambulance_speed
    if keys[pygame.K_UP]:
        ambulance_y -= ambulance_speed
    if keys[pygame.K_DOWN]:
        ambulance_y += ambulance_speed

    # 2. UPDATE STATE
    dx = ambulance_x - center_x
    dy = ambulance_y - center_y
    distance = math.sqrt(dx * dx + dy * dy)
    angle = math.atan2(dy, dx)

    # Track state changes for audio trigger
    previously_active = state["active"]
    state["active"] = (distance <= RADAR_RADIUS)
    state["distance"] = distance
    state["angle"] = angle

    # Update sweep line and blink framing
    blink_timer += 1

    # 4. SOUND (Triggered right after state evaluation)
    if state["active"] and not previously_active:
        if alert_sound:
            alert_sound.play()
        else:
            # Fallback behavior if sound file is missing
            print("\a--- SOUND: 'Caution voice' clip played! ---")

    # 3. DRAW
    # Background
    screen.fill((255, 255, 255))

    # Draw 3 concentric radar rings
    pygame.draw.circle(screen, (0, 50, 0), (center_x, center_y), RADAR_RADIUS, 2)
    pygame.draw.circle(screen, (0, 50, 0), (center_x, center_y), RADAR_RADIUS // 2, 1)
    pygame.draw.circle(screen, (0, 50, 0), (center_x, center_y), RADAR_RADIUS // 4, 1)

    # Draw the driver's car (represented as a blue square at the center)
    pygame.draw.rect(screen, (211, 211, 211), (center_x - 10, center_y - 15, 20, 30))

    # Conditional active detection overlays
    if state["active"]:
        # Blink every ~0.3 seconds (18 frames at 60 FPS)
        if (blink_timer // 18) % 2 == 0:
            # Draw red dot at ambulance location
            pygame.draw.circle(screen, (255, 0, 0), (int(ambulance_x), int(ambulance_y)), 10)
            
    else:
        # Draw the target position as a dim gray dot when out of range (for practicing placement)
        pygame.draw.circle(screen, (50, 50, 50), (int(ambulance_x), int(ambulance_y)), 6)

    # Update frame display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
