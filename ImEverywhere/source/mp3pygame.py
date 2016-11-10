import pygame.mixer
from time import sleep
pygame.mixer.init()
track = pygame.mixer.music.load("temp.mp3")
print("Play it loud,man!")
pygame.mixer.music.play(loops = -1)
pygame.mixer.music.set_volume(5.9)
sleep(2)
print("Softly does it......")
pygame.mixer.music.set_volume(0.4)
sleep(2)
track.stop()