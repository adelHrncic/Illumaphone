import serial
import time
import pygame

SERIAL_PORT = 'COM3'
BAUD_RATE = 9600
AMBIENT_FILE = r'C:\Users\Adel\OneDrive\Desktop\CS362\Illumaphone\music\fantasy.mp3'
PIANO_FILE = r'C:\Users\Adel\OneDrive\Desktop\CS362\Illumaphone\music\soft.wav'

pygame.mixer.init(frequency=44100, size=-16, channels=2)
pygame.init()

# Load sound files
try:
    print("Loading sounds...")
    ambient_sound = pygame.mixer.Sound(AMBIENT_FILE)
    piano_sound = pygame.mixer.Sound(PIANO_FILE)
except Exception as e:
    print("Failed to load sound file:", e)
    exit(1)

# Reserve channels
channel_ambient = pygame.mixer.Channel(0)
channel_piano = pygame.mixer.Channel(1)

# Connect to Arduino
print("Connecting to Arduino...")
arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)
arduino.flushInput()
print("Connected to Arduino!")

# Function to play sound on a specific channel
def play_sound(channel, sound, volume):
    sound.set_volume(volume)
    if not channel.get_busy():
        channel.play(sound)
        print(f"Playing {sound} at volume {volume}")
    else:
        print(f"{sound} is already playing.")

# Main loop
last_played_time_1 = 0
last_played_time_2 = 0
cooldown = 0.5  # seconds between sound triggers

while True:
    try:
        raw = arduino.readline()
        data_in = raw.decode(errors='ignore').strip()

        if data_in:
            tokens = data_in.split()
            if len(tokens) == 2 and all(t.isdigit() for t in tokens):
                sensor1 = int(tokens[0])
                sensor2 = int(tokens[1])
                print(f"Sensor 1: {sensor1}, Sensor 2: {sensor2}")
                now = time.time()

                # Sensor 1 triggers ambient sound
                if now - last_played_time_1 > cooldown:
                    if sensor1 < 50:
                        play_sound(channel_ambient, ambient_sound, 0.0)
                    elif sensor1 < 100:
                        play_sound(channel_ambient, ambient_sound, 0.2)
                    elif sensor1 < 250:
                        play_sound(channel_ambient, ambient_sound, 0.5)
                    elif sensor1 <= 400:
                        play_sound(channel_ambient, ambient_sound, 0.8)
                    else:
                        play_sound(channel_ambient, ambient_sound, 1.5)
                    last_played_time_1 = now

                # Sensor 2 triggers piano sound
                if now - last_played_time_2 > cooldown:
                    if sensor2 < 40:
                        play_sound(channel_piano, piano_sound, 0.0)
                    elif sensor2 < 100:
                        play_sound(channel_piano, piano_sound, 0.2)
                    elif sensor2 < 400:
                        play_sound(channel_piano, piano_sound, 0.5)
                    elif sensor2 < 500:
                        play_sound(channel_piano, piano_sound, 0.8)
                    else:
                        play_sound(channel_piano, piano_sound, 1.5)
                    last_played_time_2 = now

        pygame.time.wait(50)

    except KeyboardInterrupt:
        print("Exiting...")
        break
    except Exception as e:
        print("Error during loop:", e)
