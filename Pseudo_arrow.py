import sys
import os
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
pygame.display.set_caption("SirenSense DEMO2")
clock = pygame.time.Clock()

# Center position of the window
center_x, center_y = WIDTH // 2, HEIGHT // 2

# Configuration constants
RADAR_RADIUS = 300

# Color definitions
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (50, 50, 50)
COLOR_DIM_GRAY = (30, 30, 30)
ALERT_COLOR = (255, 0, 0)
COLOR_DARK_GREEN = (0, 40, 0)  # Color for boundary lines

# State management
state = {"active": False}
previously_active = False
current_active_direction = None
last_played_direction = None  # Prevents sound from re-triggering constantly on the same side
blink_timer = 0
alert_text = ""

lit = {
    "front": False,
    "back": False,
    "left": False,
    "right": False
}

# Practice targets (Ambulance moved via Arrow Keys)
ambulance_x = center_x + 180
ambulance_y = center_y - 180
ambulance_speed = 5

# Define the subfolder name where your audio is housed
AUDIO_FOLDER = "audio"

# Load directional audio clips from the subfolder with console fallback handling
sounds = {}
sound_files = {
    "front": "Front.mp3",
    "back": "Behind.mp3",
    "left": "Left.mp3",
    "right": "Right.mp3"
}

for direction, file_name in sound_files.items():
    # Builds the clean subfolder path (e.g., "audio/Front.mp3")
    full_path = os.path.join(AUDIO_FOLDER, file_name)
    try:
        sounds[direction] = pygame.mixer.Sound(full_path)
    except FileNotFoundError:
        sounds[direction] = None
        print(f"Warning: '{full_path}' not found. Using console fallback for {direction} alert.")

font = pygame.font.SysFont(None, 48)

# ----------------------------------------------------
# HELPER FUNCTION: DRAW CENTERED ARROW
# ----------------------------------------------------
def draw_centered_arrow(direction, color):
    """Draws a single large arrow placed exactly in the center of the window."""
    base_width = 70
    length = 80

    if direction == "front":
        points = [
            (center_x, center_y - length // 2),                  # Tip (Up)
            (center_x + base_width // 2, center_y + length // 2), # Bottom Right
            (center_x - base_width // 2, center_y + length // 2)  # Bottom Left
        ]
    elif direction == "back":
        points = [
            (center_x, center_y + length // 2),                  # Tip (Down)
            (center_x + base_width // 2, center_y - length // 2), # Top Right
            (center_x - base_width // 2, center_y - length // 2)  # Top Left
        ]
    elif direction == "left":
        points = [
            (center_x - length // 2, center_y),                  # Tip (Left)
            (center_x + length // 2, center_y - base_width // 2), # Top Right
            (center_x + length // 2, center_y + base_width // 2)  # Bottom Right
        ]
    elif direction == "right":
        points = [
            (center_x + length // 2, center_y),                  # Tip (Right)
            (center_x - length // 2, center_y - base_width // 2), # Top Left
            (center_x - length // 2, center_y + base_width // 2)  # Bottom Left
        ]
    else:
        return

    pygame.draw.polygon(screen, color, points)

# ----------------------------------------------------
# MAIN PROCESS LOOP
# ----------------------------------------------------
running = True
while running:
    # 1. HANDLE INPUT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the ambulance with Keyboard Arrow keys
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

    previously_active = state["active"]
    state["active"] = (distance <= RADAR_RADIUS)

    # Reset active tracking elements
    for key in lit:
        lit[key] = False
    
    alert_text = ""
    current_active_direction = None

    # Determine which direction arrow should flash using exclusive if-elif branches
    if state["active"] and distance > 0:
        right_amount = dx / distance
        left_amount = -dx / distance
        back_amount = dy / distance  
        front_amount = -dy / distance

        if front_amount >= back_amount and front_amount >= left_amount and front_amount >= right_amount:
            lit["front"] = True
            current_active_direction = "front"
            #alert_text = "CAUTIOUS, VEHICLE AHEAD"
        elif back_amount >= front_amount and back_amount >= left_amount and back_amount >= right_amount:
            lit["back"] = True
            current_active_direction = "back"
            #alert_text = "AMBULANCE BEHIND: MERGE AWAY"
        elif left_amount >= front_amount and left_amount >= back_amount and left_amount >= right_amount:
            lit["left"] = True
            current_active_direction = "left"
            #alert_text = "CAUTIOUS, VEHICLE ON LEFT"
        else:
            lit["right"] = True
            current_active_direction = "right"
            #alert_text = "CAUTIOUS, VEHICLE ON RIGHT"

    # Reset sound gate if the ambulance completely leaves range
    if not state["active"]:
        last_played_direction = None

    blink_timer += 1
    blink_is_on = (blink_timer // 18) % 2 == 0

    # 4. SOUND TRIGGER LOGIC
    if state["active"] and current_active_direction != last_played_direction:
        sound_clip = sounds.get(current_active_direction)
        
        if sound_clip:
            sound_clip.play()
        else:
            print(f"\a--- VOICE ALERT: 'Caution, emergency vehicles {current_active_direction}' ---")
            
        last_played_direction = current_active_direction

    # 3. DRAW
    screen.fill(COLOR_BLACK)

    # Visual Layout References (Square Center Box & Active Detection Radius Circle)
    pygame.draw.rect(screen, COLOR_DARK_GREEN, (center_x - 40, center_y - 40, 80, 80), 1)
    pygame.draw.circle(screen, COLOR_DARK_GREEN, (center_x, center_y), RADAR_RADIUS, 1)

    # Render the active direction arrow directly in the center during the blink "on" phase
    if blink_is_on:
        for direction in ["front", "back", "left", "right"]:
            if lit[direction]:
                draw_centered_arrow(direction, ALERT_COLOR)

    # Render context dashboard text alert
    if state["active"] and alert_text != "":
        text_surface = font.render(alert_text, True, ALERT_COLOR)
        text_rect = text_surface.get_rect(center=(center_x, 100))
        screen.blit(text_surface, text_rect)

    # Practice corner mini-view mapping window
    mini_box = pygame.Rect(WIDTH - 110, 10, 100, 100)
    pygame.draw.rect(screen, COLOR_DIM_GRAY, mini_box, 1)
    
    scale_factor = 100 / 800
    mini_amb_x = mini_box.left + int(ambulance_x * scale_factor)
    mini_amb_y = mini_box.top + int(ambulance_y * scale_factor)
    
    mini_amb_x = max(mini_box.left, min(mini_amb_x, mini_box.right))
    mini_amb_y = max(mini_box.top, min(mini_amb_y, mini_box.bottom))
    
    pygame.draw.circle(screen, COLOR_GRAY, (mini_amb_x, mini_amb_y), 4)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
