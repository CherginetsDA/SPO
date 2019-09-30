# SPO Чергинец Дмитрий гр. R3336
---
## Lab1 
### Задание
Необходимо написать скрипт, который создает таблицу с данными о содержащихся в директории файлах. В таблице обязательно должны присутствовать следующие столбцы:
*название файла;
*расширение файла;
*дата изменения;
*размер (желательно в МБ);
*длительность аудио и видео файлов.

### Запуск
Для запуска введите
<./lab_1.sh directory>
> direcory - папка которую необходимо проверить

> При отсутствии libreoffice необходимо установить утилиту ssconvert. Это можно сделать следующим образом:

##### Ubuntu
<sudo apt-get install gnumeric>
  
##### Arch linux
<sudo pacman -S gnumeric>

> Данный скрипт проверялся на Ubuntu 18.04 и Arch linux
---
## Lab2
### Задание
Необходимо реализовать bash скрипт, который будет загружать на ваш компьютер проект с репозитория GitHub с последующей его сборкой и расположением файлов в системные папки
> В моем случае это <https://github.com/cjdelisle/cjdns>

### Запуск
Для запуска введите
<./lab_2.sh>

> По оканчанию исполнения скрипта cjdns будет находиться в системной папке /opt

> Если скрипт запускается из системной папки добавте sudo

>Данный скрипт работает на Ubuntu 18.04, но при установленных всех необходимых пакетах также работает и на Arch linux
