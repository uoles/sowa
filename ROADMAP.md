#### TODO:
 
    - Разделить код на классы 
        управление совой
        вывод аудио
        запись команд
        справочники
        вспомогательные утилиты
    - Сделать воспроизведение аудио по времени и дням недели 
        19:00 пн-чт     "пора домой"
        19:00 пт        "пошли в фусян"
        12:00 пн-пт     "пошли на стендап"
        13:00 пн-пт     "пора пожрать"
    - Реализовать web-морду для управления настройками
        вкл/выкл реакции крылом
        вкл/выкл реакции звуком
        редактирование справочника для реакции крылом
        редактирование справочника для реакции звуком

#### Реализовано:

---
2024-02-08 Попытка исправить ошибку "ALSA lib pcm.c:8545:(snd_pcm_recover) underrn occurred".
- Установил PulseAudio (https://forums.raspberrypi.com/viewtopic.php?t=62851)
```
sudo apt-get install pulseaudio
sudo apt-get install pavucontrol paprefs
sudo reboot
```
Результат: звук стал хуже.

- Отключил PulseAudio (https://forums.raspberrypi.com/viewtopic.php?t=30108) 
```
в конфиге /etc/pulse/client.conf выставил autospawn = no
sudo reboot
``` 
Результат: при запуске скрипта совы перестал находить устройство вывода.

- Выбор устройства (https://stackoverflow.com/questions/64393732/how-do-i-change-the-audio-output-device-from-the-command-line-in-raspbian) 
    sudo amixer cset numid=3 n,
    где n - 0=auto, 1=headphones, 2=hdmi.
```
sudo amixer cset numid=3 1
sudo reboot
```
Результат: воспроизведение нормальное, наличие ошибки нужно проверять.

---
2024-02-05 Убрал ошибку "ERROR:root:Failed getting command: [Errno -9981] Input overflowed".
- При чтении данных из потока выставил параметр exception_on_overflow=False.
```
data = stream.read(4096, exception_on_overflow=False)
```
Результат: ошибка ушла.

- Отключил расписание с шедулером, нужно дорабатывать.
---