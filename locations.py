# TODO: тут надо поменять пути на def

# все файлы надо хранить в папке, в которую поставили secure-file-priv в конфиге MAMP
# main_path отвечает за путь к папке, остальные переменные формируют файлы для загрузки их в базу
main_path = "/Users/vladislavsyrockin/Desktop/AstroData/" # пример пути "C:\\\\Users\\\\vladislavsyrockin\\\\Desktop\\\\Astro\\\\"

ucac2_bin_filename = main_path + "ucac2.bin" # отвечает за каталог ucac-2 бинарный. ссылка для скачивания(https://drive.google.com/file/d/1Z5DElVsTt60BGaj_5BYqQy8SgemsWiR-/view?usp=sharing)
ucac2_txt_filename = main_path + "ucac2.txt"

tycho_txt_filename = main_path + "catalog.dat" # отвечает за каталог tycho-2 текстовый. ссылка для скачивания(http://archive.eso.org/ASTROM/TYC-2/data/)

sql_out_compare_filename = main_path + "compare.txt"
sql_out_delta2_filename = main_path + "delta2.txt"
sql_out_delta3_filename = main_path + "delta3.txt"
sql_out_delta4_filename = main_path + "delta4.txt"
sql_out_delta5_filename = main_path + "delta5.txt"
sql_out_delta6_filename = main_path + "delta6.txt"
sql_out_answers_filename = main_path + "answers.txt"
sql_out_filename_example = main_path + "example"

_en = True  # эту переменную трогать не надо
db_port = "8889" # порт по умолчанию для windows - "3306"
process_count = 6
