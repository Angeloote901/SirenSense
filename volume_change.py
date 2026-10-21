import time
import pygame

# Initialize the pygame sound engine
pygame.mixer.init()

# 1. Load your audio tracks
car_track = pygame.mixer.Sound("inside_car_sound.mp3")
ambulance_track = pygame.mixer.Sound("49053354-ambulance-312230.mp3")
music_track = pygame.mixer.Sound("background_music.mp3")  # Added music file

# 2. Assign them to independent audio channels
car_channel = pygame.mixer.Channel(0)
ambulance_channel = pygame.mixer.Channel(1)
music_channel = pygame.mixer.Channel(2)  # Added a 3rd dedicated channel

# --- Step 1: Start the music and car engine normally ---
print("🎵 Background music starts playing softly...")
music_channel.set_volume(0.15)  # Keeping it at a gentle background level
music_channel.play(music_track, loops=-1)  # Loop forever

print("🚗 The car engine starts humming steadily in the cabin...")
car_channel.set_volume(0.6)  # Keep the car at a steady 60% volume
car_channel.play(car_track, loops=-1)  # Loop forever

time.sleep(15)  # Drive normally with music for 15 seconds

# --- Step 2: The ambulance approaches (starts quiet at 20%) ---
print("🔈 🚨 Ambulance siren heard faintly in the distance (20%)...")
ambulance_channel.set_volume(0.2)
ambulance_channel.play(ambulance_track)

time.sleep(4)  # Let it stay distant for 4 seconds

# --- Step 3: The ambulance passes right by you (increases to 100%) ---
print("🔊 🚨 Ambulance zooming past! Screaming up to 100% volume...")
for v in range(20, 101, 4):
    ambulance_channel.set_volume(v / 100.0)
    time.sleep(0.04)  # Smooth transition

time.sleep(2.5)  # Peak loudness as it drives beside you

# --- Step 4: The ambulance drives away (fades down to 40%) ---
print("🔉 🚨 Siren fading into the distance ahead (dropping to 40%)...")
for v in range(100, 39, -4):
    ambulance_channel.set_volume(v / 100.0)
    time.sleep(0.04)

print("🎵 Keeping it steady at 40% as it pulls ahead...")
time.sleep(10)  # Play out the rest of the scene

# Clean up and stop all audio layers at once
pygame.mixer.stop()
print("✅ Scene finished!")
