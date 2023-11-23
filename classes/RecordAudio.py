#!/usr/bin/python3
import json
import queue
from threading import Thread

import pyaudio
from vosk import Model, KaldiRecognizer


class RecordAudio(Thread):

    chunk = 16000
    rate = 16000
    seconds = 60

    model = Model(r"../vosk-model-small-ru-0.221")
    recognizer = KaldiRecognizer(model, chunk)

    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16,
                      channels=1,
                      rate=rate,
                      frames_per_buffer=chunk,
                      input_device_index=1,
                      input=True)

    frames = queue.Queue(maxsize=20)

    # инициализация объекта потока
    def __init__(self, event) -> None:
        super().__init__()
        self.event = event

    # запуск потока
    def run(self) -> None:
        try:
            self.process()
        finally:
            print('RecordAudio stopped...')

    # получение данных с микрофона и распознавание слов
    def process(self):
        is_running_process = True
        while is_running_process:
            for i in range(0, int(self.rate / self.chunk * self.seconds)):
                if self.event.is_set():
                    is_running_process = False
                    self.on_quit()
                    break

                try:
                    data = self.stream.read(self.chunk)
                    if len(data) > 0:
                        if self.recognizer.AcceptWaveform(data):
                            inputStr = self.recognizer.Result()
                        else:
                            inputStr = self.recognizer.PartialResult()

                        command = json.loads(inputStr)
                        partial = command.get("partial")

                        result = ''
                        if partial:
                            result = command["partial"]
                        else:
                            result = ''
                        self.frames.put(result)
                except Exception as e:
                    print(e)
                    self.mic_stream_close()
                    self.mic_stream_open()
                    pass

    # открыть поток с микрофона
    def mic_stream_open(self):
        self.stream = self.mic.open(format=pyaudio.paInt16,
                                    channels=1,
                                    rate=self.rate,
                                    frames_per_buffer=self.chunk,
                                    input_device_index=1,
                                    input=True)

    # закрыть поток с микрофона
    def mic_stream_close(self):
        self.stream.close()

    # закрываем объекты
    def on_quit(self):
        self.stream.stop_stream()
        self.stream.close()
        self.mic.terminate()

    # возвращает очередь с распознанными словами
    def get_frames(self):
        return self.frames

    # возвращает команду
    def get_command(self):
        command = self.frames.get()
        self.frames.task_done()
        return command
