import time
from playsound3 import playsound

print("🚗 Starting the car sound in the background...")
# block=False tells Python to play this sound WITHOUT stopping the code execution
playsound("inside_car_sound.mp3", block=False)

# Give the car sound a 2-second head start before the ambulance joins in
time.sleep(5)

print("🚨 Overlapping the ambulance sound now!")
# This plays the ambulance sound at the exact same time the car is playing
playsound("49053354-ambulance-312230.mp3")

print("✅ Finished handling playback commands!")
