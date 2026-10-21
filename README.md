# SirenSense

For elderly and hard-of-hearing drivers, pinpointing a sudden siren is a dangerous challenge that often leads to panic, delayed reactions, and accidents. I am developing an assistive vehicle feature or device that visually flags approaching first responders. This critical solution gives seniors the extra time they need to navigate the roads calmly and pull over safely.

## Whereto look

This repo contains two demos of the device. These are the files to run: 

Files:
'pseudo_radar.py' | Radar Version, where the driver is in the middle and when the emergency vehicle enters the detected radius, you will see a blinking dot that shows the location of the vehicle.

'Pseudo_arrow.py' | Arrow Version, Four directional arrows (Front, Back, Left, Right) light up and blink toward where the vehicle is coming from. 

Both give a visual alert and announce the "Cautious, Pull over safely" or the location of the vehicle.

## How to run program: 

Install the dependency: 
```
pip install pygame
```
Run either demo:
```
python pseudo_radar.py
python Pseudo_arrow.py
```

## Controls

The emergency vehicle is simulated. Move it yourself to test the alerts:
- **Radar demo:** arrow keys
- **Arrow demo:** arrow keys

## Audio

Keep the audio files in the project folder, since the demos look for them when they start. If one is missing, the demo prints a message in the terminal instead of playing sound.
