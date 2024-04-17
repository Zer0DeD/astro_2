# insert ucac-2 to mysql table
import os

import base
import locations
import struct
import re
import io
from multiprocessing import Process


def read_file(sql_file_out_name, catalog_name, thread_id):
    format1 = 'i'
    format2 = 'h'

    count = 0
    thread_count = 0

    catalog = io.open(catalog_name, "rb")
    out_file = io.open(sql_file_out_name, "w", newline='\n')

    while True:
        if count % 10000000 == 0:
            print(f"Complited {count} - Thread Id = {thread_id}")

        count += 1

        if not count % locations.process_count == thread_id:
            data = catalog.read(44)
            continue

        try:
            data = catalog.read(4)
            ra = struct.unpack(format1, data)

            data = catalog.read(4)
            dec = struct.unpack(format1, data)

            data = catalog.read(2)
            mag = struct.unpack(format2, data)

            data = catalog.read(34)
        except:
            break
        if not re.search('\d+', str(ra[0])) or not re.search('\d+', str(dec[0])) or not re.search('\d+', str(mag[0])):
            continue

        out = f"{ra[0] * 2.7777776630942e-7};{dec[0] * 2.7777776630942e-7};{mag[0] / 100}\n"

        thread_count += 1
        out_file.write(out)

    catalog.close()
    out_file.close()

    print(f"Complited. Total {thread_count} lines - Thread Id = {thread_id}")


def main():
    base.cw_start("Insert UCAC-2")
    base.cw("Start creating catalog file")
    db = base.DBHConnection()

    cursor = db.cursor_execute("DROP TABLE IF EXISTS ucac2")
    cursor = db.cursor_execute(
        "CREATE TABLE `ucac2` ( `star_id` INT NOT NULL AUTO_INCREMENT , `mean_ra` DOUBLE NOT NULL , `mean_dec` DOUBLE NOT NULL , `mag` DOUBLE NOT NULL , UNIQUE `id` (`star_id`)) ENGINE = InnoDB;")

    prc = []
    out_filenames = []
    for i in range(locations.process_count):
        out_filenames.append(locations.sql_out_filename_example + f"{i}" + ".txt")

    for i in range(locations.process_count):
        pr = Process(target=read_file, args=(out_filenames[i], locations.ucac2_bin_filename, i,))
        prc.append(pr)
        pr.start()

    for pr in prc:
        pr.join()

    file = open(locations.ucac2_txt_filename, 'w')
    file.close()

    for i in range(locations.process_count):
        file = open(locations.ucac2_txt_filename, 'a')
        file_ = open(out_filenames[i], 'r')
        for line in file_:
            file.write(line)
        file_.close()
        file.close()

    base.cw(f"Finished creating catalog file")
    base.cw("Start loading database")

    cursor = db.cursor_execute(
        f"LOAD DATA INFILE '{locations.ucac2_txt_filename}' INTO TABLE ucac2 FIELDS TERMINATED BY ';' (mean_ra,mean_dec,mag) SET star_id=NULL;")
    cursor = db.cursor_execute("ALTER TABLE ucac2 ADD INDEX `coord` (`mean_ra`, `mean_dec`, `mag`);")

    base.cw("Finished loading database")
    base.cw_finish()


if __name__ == "__main__":
    main()
