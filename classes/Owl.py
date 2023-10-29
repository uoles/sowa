import collections
import logging
import threading
import tracemalloc

from PlayAudio import PlayAudio
from Controller import Controller
from RecordAudio import RecordAudio
from Utils import Utils

# log
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# starting the monitoring
tracemalloc.start()


# показывает размер занимаемой памяти
def show_memory():
    currentMem, peakMem = tracemalloc.get_traced_memory()
    print('==== currentMem: ' + str(currentMem) + ', peakMem: ' + str(peakMem))


class Owl:

    last_commands = collections.deque(maxlen=5)
    bad_words = set()
    audio_reactions = set()

    controller = Controller()
    play_audio = PlayAudio()
    event = threading.Event()
    record_audio = RecordAudio(event)

    def __init__(self, reaction_wing_enabled, reaction_audio_enabled):
        self.bad_words = Utils.bad_words_load('../static/bad_words.txt')
        self.audio_reactions = Utils.audio_reactions_load('../static/audio_reaction.json')
        self.reaction_wing_enabled = reaction_wing_enabled
        self.reaction_audio_enabled = reaction_audio_enabled
        self.controller.sowa_wing_down()
        self.record_audio.start()

    def get_controller(self):
        return self.controller

    # реагирование на команды
    def reaction(self, input_words):
        # реакция крылом
        if self.reaction_wing_enabled:
            if Utils.compare_lists(input_words, list(self.bad_words)):
                self.controller.sowa_wing_up()
                threading.Timer(3.0, self.controller.sowa_wing_down()).start()

        # реакция звуком
        if self.reaction_audio_enabled:
            for item in self.audio_reactions:
                if Utils.compare_lists(input_words, item.get('words')):
                    self.play_audio.play(item.get('audio'))

    def on_quit(self):
        self.controller.close()
        self.event.set()
        self.record_audio.join()

    # основная процедура получения и обработки команд
    def process(self):
        last_input_words = set()

        while True:
            try:
                input_words = list()
                if not self.play_audio.is_busy() and not self.controller.is_wing_down():
                    self.play_audio.stop()
                    command = self.record_audio.get_command()
                    # удаляем из списка слова предыдущего списка
                    input_words = Utils.check_command(command, self.last_commands)

                # проверяем на наличие слов в списке
                # дополнительно проверяем, что список слов отличается от предыдущего списка
                # (!!! существуют ситуации, когда прилетает такой же список слов, как и предыдущий !!!)
                if input_words and len(input_words) > 0 and not (last_input_words == input_words):
                    print('command: ' + str(input_words))
                    self.reaction(input_words)

                    for word in input_words:
                        self.last_commands.append(word)
                    print('last_commands: ' + str(self.last_commands))

                    last_input_words.clear()
                    last_input_words = set(input_words)

                    show_memory()
                    print('=======================================')
            except KeyboardInterrupt:  # Exit ctrl+c
                self.on_quit()
                raise SystemExit
            except Exception as e:
                log.error('process()::exception: %s', e)


if __name__ == '__main__':
    try:
        owl = Owl(False, True)
        owl.process()
    except Exception as e:
        log.error('main()::exception: %s', e)