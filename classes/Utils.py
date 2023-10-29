#!/usr/bin/python3
import json


class Utils:

    # загрузка справочника для реакции крылом
    @staticmethod
    def bad_words_load(file_path):
        words = []
        print('Загружаем справочник слов...')
        with open(file_path, 'r', encoding='utf-8') as infile:
            for line in infile:
                words.append(line.replace('\n', ''))
        print(words)
        return set(words)

    # загрузка справочника для реакции звуком
    @staticmethod
    def audio_reactions_load(file_path):
        print('Загружаем справочник аудио реакций...')
        with open(file_path, 'r', encoding='utf-8') as fJson:
            data = json.load(fJson)
        return data['items']

    # проверка наличия списка новых слов в другом списке слов
    @staticmethod
    def compare_lists(input_words, expected):
        result = False
        set_input_words = set(input_words)
        set_expected = set(expected)
        if set_expected.intersection(set_input_words):
            result = True
        return result

    # выделяет слова, которые есть в новом потоке и нет в старом
    @staticmethod
    def exclude_words(command, last_command):
        list_command = set(command)
        list_last_command = set(last_command)
        return list_command.difference(list_last_command)

    # проверка команд
    @staticmethod
    def check_command(command, last_commands):
        result = list()
        # проверяем, что в строке больше 1 символа
        if command and len(command.replace(' ', '')) > 1:
            list_command = command.split(' ')
            list_last_commands = list(last_commands)
            # удаляем из списка новых слов слова предыдущего списка
            result = list(OwlUtils.exclude_words(list_command, list_last_commands))
        return result
