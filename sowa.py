#!/usr/bin/python3
import sys
import logging
import json
import threading

from pymodbus.client.serial import ModbusSerialClient as ModbusClient
from vosk import Model, KaldiRecognizer

import pyaudio
import pygame

from sowa_utils import sowa_utils

# log
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# load Vosk library
model = Model(r"vosk-model-small-ru-0.22")
recognizer = KaldiRecognizer(model, 16000)

# create microphone stream
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input_device_index=1, input=True, frames_per_buffer=16000)
stream.start_stream()

# create connection (boot mode is 9600)
client = ModbusClient(method='rtu', port='/dev/ttyACM0', baudrate=230000, timeout=1.5)
client.connect()

# init PyGame for audio output
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)

idslave = 0x01
lastCommand = ''
isWingDown = True


def play_audio(audioFileName):
    print('play_audio: ' + str(audioFileName))
    pygame.mixer.music.load('static/audio/' + audioFileName)
    pygame.mixer.music.play()


def get_command():
    try:
        data = stream.read(4096)
        if len(data) != 0:
            inputStr = ""
            if recognizer.AcceptWaveform(data):
                inputStr = recognizer.Result()
            else:
                inputStr = recognizer.PartialResult()

            command = json.loads(inputStr)
            partial = command.get("partial")
            result = ""
            if (partial):
                result = command["partial"]

            return result
    except OSError:
        pass


def send_value(newValue):
    print('send new value: ' + str(newValue))
    client.write_register(address=0x0000, value=newValue, slave=idslave)


def sowa_wing_up():
    global isWingDown
    send_value(100)
    isWingDown = False


def sowa_wing_down():
    global isWingDown, lastCommand
    send_value(0)
    isWingDown = True
    lastCommand = ''
    print('=======================================')


def process_command(value):
    input_words = value.split(" ")
    print('input_words: ' + str(input_words))

    # реакция звуком
    for item in audio_reactions:
        if compare_lists(input_words, item.get('words')):
            print('command: ' + str(value))
            play_audio(item.get('audio'))

    # реакция крылом
    if bad_words_contains(input_words):
        print('command: ' + str(value))
        sowa_wing_up()
        threading.Timer(5.0, sowa_wing_down).start()


def bad_words_contains(input_words):
    set_input_words = set(input_words)
    if bad_words.intersection(set_input_words):
        return True
    else:
        return False


def compare_lists(input_words, expected):
    set_input_words = set(input_words)
    set_expected = set(expected)
    if set_expected.intersection(set_input_words):
        return True
    else:
        return False


def on_quit():
    print('\nПрограмма завершена')
    stream.stop_stream()
    stream.close()
    mic.terminate()
    sys.exit()


bad_words = sowa_utils.bad_words_load()
audio_reactions = sowa_utils.audio_reactions_load()

sowa_wing_down()
while True:
    try:
        command = get_command()
        if isWingDown and command and len(command) != 0 and command != lastCommand:
            process_command(command)
            lastCommand = command
            print('=======================================')
    except KeyboardInterrupt:  # Exit ctrl+c
        on_quit()
        raise SystemExit
    except Exception:
        tb = sys.exception().__traceback__
        print('Exception: ' + str(tb))
        pass
