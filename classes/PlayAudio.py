#!/usr/bin/python3
import pygame


class PlayAudio:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(1.0)

    def play(self, audioFileName):
        print('play_audio: ' + str(audioFileName))
        pygame.mixer.music.load('../static/audio/' + audioFileName)
        pygame.mixer.music.play()

    def is_busy(self):
        return pygame.mixer.music.get_busy()

    def stop(self):
        pygame.mixer.music.stop()
