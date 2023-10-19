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