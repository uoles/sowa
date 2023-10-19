#!/usr/bin/python3
import json

class sowa_utils:

    @staticmethod
    def bad_words_load():
        words = []
        print('Загружаем справочник слов...')
        with open('static/bad_words.txt', 'r', encoding='utf-8') as infile:
            for line in infile:
                words.append(line.replace('\n', ''))
        print(words)
        return set(words)

    @staticmethod
    def audio_reactions_load():
        print('Загружаем справочник аудио реакций...')
        with open('static/audio_reaction.json', 'r', encoding='utf-8') as fJson:
            data = json.load(fJson)
        return data['items']
