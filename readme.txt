Нужно для работы кода:
1. Установить Python версии 3.11 или выше (https://www.python.org)
2. Установить PyCharm Community или другую любую среду разработки (https://www.jetbrains.com/ru-ru/pycharm/)
3. установить MAMP для работы с MySQL (https://www.mamp.info/en/)
3.1 По умолчанию порт под windows 3306, можно не менять
3.2 Для MAMP под Windows надо в директории "C:\MAMP\conf\mysql" зайти в конфиг my.ini и прописать дополнительный параметр:
    # The MySQL server
    [mysqld]
    port		= 3306
    socket		= mysql
    skip-external-locking
    key_buffer_size = 16M
    max_allowed_packet = 1M
    table_open_cache = 64
    sort_buffer_size = 512K
    net_buffer_length = 8K
    read_buffer_size = 256K
    read_rnd_buffer_size = 512K
    myisam_sort_buffer_size = 8M
    secure-file-priv="путь к папке с файлами" # вот только эту строчку надо добавить (пример: "C:\\Users\\user\\Desktop\\Astro")
    basedir = C:/MAMP/bin/mysql/
    datadir = C:/MAMP/db/mysql/
    character-set-server=utf8
    collation-server=utf8_general_ci
3.3 После запуска MAMP надо убедиться, что MySQL server запущен, для этого можно перейти по ссылке (http://localhost/phpMyAdmin/)
3.4 Тут надо создать новую директорию с именем "astro"
4. В файле locations.py надо поменять переменные, они подписаны
5. Файлы tycho-2 и ucac-2 можно скачать по ссылкам в файле locations.py. Их надо поместить в ту же папку, куда указывали путь для secure-file-priv
6. Перед запуском кода надо проверить установленные библиотеки, для этого надо открыть терминал в PyCharm и ввести команду:
pip list
если в выданном списке есть mysql.connector, то все нормально, но если его нет, то надо прописать:
pip install mysql.connector
7. После этого надо запустить скрипт в том же терминале с помощью команды:
python3 run_all_python3.py (выполнение скрипта занимает около часа)
если не работает, то запустите:
python run_all_python.py
