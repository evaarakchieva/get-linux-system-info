# Приложение для сбора информации о системе Linux
Приложение выполняет несколько функций:
- сбор информации о процессе,  в котором оно запущено (количество дескрипторов, потребление памяти, путь к исполняемому файлу)
- сбор информации о процессоре (модель, количество ядер)
- сбор информации о памяти (всего, доступно, использовано)
- сбор информации о дисках (модель, размер, количество свободного места)
- сбор информации о cgroups (имя контроллера, значение)

Программа выводит все в файл JSON

Dockerfile собирает образ приложения для запуска в контейнере
