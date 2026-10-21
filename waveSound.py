import numpy as np
import sounddevice as sd

# Configurations
sample_rate = 44100  # CD Quality standard Hz
duration = 2.0  # Seconds
frequency = 440.0  # A4 tone in Hz

# Generate a timeline array
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Create a sine wave array
audio_wave = 0.5 * np.sin(2 * np.pi * frequency * t)

print("Playing sound... Please ensure your speakers are on and volume is up.")
# Play the synthesized array directly through your speakers
sd.play(audio_wave, sample_rate)
sd.wait()  # Wait until the wave finishes playing

print("sound playback finished.")