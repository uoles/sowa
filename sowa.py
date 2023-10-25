#!/usr/bin/python3
import collections
import sys
import logging
import json
import threading

from pymodbus.client.serial import ModbusSerialClient as ModbusClient
from vosk import Model, KaldiRecognizer

import pyaudio
import pygame
import tracemalloc

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
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input_device_index=1, input=True,
                  frames_per_buffer=16000)

# create connection (boot mode is 9600)
client = ModbusClient(method='rtu', port='/dev/ttyACM0', baudrate=230000, timeout=1.5)
client.connect()

# init PyGame for audio output
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)

# starting the monitoring
tracemalloc.start()

idslave = 0x01
isWingDown = True
bad_words = sowa_utils.bad_words_load()
audio_reactions = sowa_utils.audio_reactions_load()
last_commands = collections.deque(maxlen=5)


# проиграть аудио файл
def play_audio(audioFileName):
    print('play_audio: ' + str(audioFileName))
    pygame.mixer.music.load('static/audio/' + audioFileName)
    pygame.mixer.music.play()


# считать команды с микрофона
def get_command():
    try:
        result = ""
        data = stream.read(4096)
        if len(data) != 0:
            inputStr = ""
            if recognizer.AcceptWaveform(data):
                inputStr = recognizer.Result()
            else:
                inputStr = recognizer.PartialResult()

            command = json.loads(inputStr)
            partial = command.get("partial")

            if (partial):
                result = command["partial"]

            return result
    except Exception as e:
        log.error('Failed getting command: %s', e)
        mic_stream_close()
        mic_stream_create()
        pass


# открыть поток с микрофона
def mic_stream_create():
    global stream
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input_device_index=1, input=True,
                      frames_per_buffer=16000)


# закрыть поток с микрофона
def mic_stream_close():
    stream.close()


# отправить значение в контроллер крыла совы
def send_value(newValue):
    print('send new value: ' + str(newValue))
    client.write_register(address=0x0000, value=newValue, slave=idslave)


# поднять крыло совы
def sowa_wing_up():
    global isWingDown
    send_value(100)
    isWingDown = False


# опустить крыло совы
def sowa_wing_down():
    global isWingDown
    send_value(0)
    isWingDown = True
    print('=======================================')


# реагирование на команды
def reaction(input_words):
    # реакция крылом
    if bad_words_contains(input_words):
        sowa_wing_up()
        threading.Timer(3.0, sowa_wing_down).start()

    # реакция звуком
    for item in audio_reactions:
        if compare_lists(input_words, item.get('words')):
            play_audio(item.get('audio'))


# сравнение входящих слов со списком слов для реакции крылом
def bad_words_contains(input_words):
    set_input_words = set(input_words)
    if bad_words.intersection(set_input_words):
        return True
    else:
        return False


# сравнение списков
def compare_lists(input_words, expected):
    set_input_words = set(input_words)
    set_expected = set(expected)
    if set_expected.intersection(set_input_words):
        return True
    else:
        return False


# завершение программы
def on_quit():
    print('\nПрограмма завершена')
    stream.stop_stream()
    stream.close()
    mic.terminate()
    tracemalloc.stop()
    client.close()
    sys.exit()


# показывает размер занимаемой памяти
def show_memory():
    currentMem, peakMem = tracemalloc.get_traced_memory()
    print('==== currentMem: ' + str(currentMem) + ', peakMem: ' + str(peakMem))


# основная процедура получения и обработки команд
def process():
    global last_commands
    while True:
        try:
            input_words = list()
            if not pygame.mixer.music.get_busy() and isWingDown:
                pygame.mixer.music.stop()
                command = get_command()
                input_words = check_command(command)

            if input_words and len(input_words) > 0:
                print('command: ' + str(input_words))
                reaction(input_words)

                for word in input_words:
                    last_commands.append(word)
                print('last_commands: ' + str(last_commands))

                show_memory()
                print('=======================================')
        except KeyboardInterrupt:  # Exit ctrl+c
            on_quit()
            raise SystemExit
        except Exception as e:
            log.error('Failed processing: %s', e)


# выделяет слова, которые есть в новом потоке и нет в старом
def exclude_words(command, last_command):
    list_command = set(command)
    list_last_command = set(last_command)
    return list_command.difference(list_last_command)


# проверка команды
def check_command(command):
    result = list()
    if command and len(command) > 1:
        list_command = command.split(" ")
        list_last_commands = list(last_commands)
        result = list(exclude_words(list_command, list_last_commands))
    return result


if __name__ == '__main__':
    try:
        sowa_wing_down()
        process()
    except Exception as e:
        log.error('Main failed processing: %s', e)