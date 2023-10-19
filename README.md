Настройка USB микрофона на raspberry pi:
https://notalentgeek.github.io/note/note/project/project-commitment/pc-ut-bachelor-thesis-2016/reading/20170105-0159-cet-how-to-connect-usb-microphone-into-pyaudio-in-raspbian-jessie/

Инфо:
https://classes.engineering.wustl.edu/ese205/core/index.php?title=Audio_Input_and_Output_from_USB_Microphone_%2B_Raspberry_Pi

Запуск скрипта при старте raspberry pi:
https://stackoverflow.com/questions/24518522/run-python-script-at-startup-in-ubuntu
----------------------------------------------------------------------------
Показывает список устройств вывода:
aplay -l
----------------------------------------------------------------------------
https://projects-raspberry.com/getting-audio-out-working-on-the-raspberry-pi/

sudo apt-get install alsa-utils
sudo apt-get install mpg321
sudo apt-get install lame
----------------------------------------------------------------------------
> Не делать, отключается микрофон: >> amixer cset numid=3 1
----------------------------------------------------------------------------
https://raspberrytips.com/create-image-sd-card/
http://cagewebdev.com/raspberry-pi-getting-audio-working/
https://www.bareconductive.com/blogs/resources/how-to-change-the-volume-on-the-pi-cap
----------------------------------------------------------------------------
2023-12-19:
* исправлена ошибка обработки только первого слова из фразы
* добавлено воспроизведение аудио записей как рекция на слово

* Проблема:
через какое-то время приложение выдает ошибку

ALSA lib pcm.c:8545:(snd_pcm_recover) underrun occurred
ALSA lib pcm.c:8545:(snd_pcm_recover) underrun occurred
ALSA lib pcm.c:8545:(snd_pcm_recover) underrun occurred

* Проблема:
периодически перестает работать микрофон, закрывается stream

* Проблема:
есть утечка памяти при отправке данных в контроллер для реакции крылом

* Проблема:
через какое-то время приложение выдает ошибку

ERROR:root:Failed getting command: [Errno -9981] Input overflowed

Решение - 1:
сделать реинициализацию stream
Решение - 2:
https://github.com/alphacep/vosk-api/issues/128