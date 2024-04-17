##compare ucac-2 and tycho-2 and calculating delta 1
import os

import base
import locations
import re
import io
from multiprocessing import Process

delta = 1 / 60 / 60
delta_mag = 1


def compare(out, catalog, thread_id):
    global delta
    global delta_mag
    db_local = base.DBHConnection()

    tycho_2_file = io.open(catalog, 'r')
    out_file = io.open(out, 'w', newline='\n')

    count = 0
    thread_count = 0

    for line in tycho_2_file:
        if count % 300000 == 0:
            print(f"Complited {count} lines - Thread Id = {thread_id}")

        count += 1
        if not count % locations.process_count == thread_id:
            continue

        if not re.search("^\d+", line):
            continue

        line = re.sub("\n|\r|\s+", "", line)

        str = line.split('|')

        if not re.search('\d+', str[2]) or not re.search('\d+', str[3]) or not re.search('\d+',
                                                                                         str[17]) or not re.search(
            '\d+', str[19]):
            continue

        ra = float(str[2])
        ra_plus = ra + delta
        ra_minus = ra - delta
        dec = float(str[3])
        dec_plus = dec + delta
        dec_minus = dec - delta
        mag_bt = float(str[17])
        mag_bt_plus = mag_bt + delta_mag
        mag_bt_minus = mag_bt - delta_mag
        mag_vt = float(str[19])

        sql_query = f"""SELECT mean_ra, mean_dec, mag FROM ucac2                                                                        
                WHERE mean_ra BETWEEN {ra_minus} AND {ra_plus}                                                       
                AND mean_dec  BETWEEN {dec_minus} AND {dec_plus}                                                     
                AND mag    BETWEEN {mag_bt_minus} AND {mag_bt_plus} LIMIT 5"""
        cursor = db_local.cursor_execute(sql_query)

        if cursor.rowcount != 1:
            continue

        res = cursor.fetchone()
        ra_ucac = res[0]
        dec_ucac = res[1]
        mag_ucac = res[2]

        delta_a1 = abs(abs(ra) - abs(ra_ucac))
        delta_d1 = abs(abs(dec) - abs(dec_ucac))

        if locations._en:
            out = f"{ra};{dec};{mag_bt};{mag_vt};{ra_ucac};{dec_ucac};{mag_ucac};{abs(delta_a1)};{abs(delta_d1)}\n"
        else:
            out = f"{ra};{dec};{mag_bt};{mag_vt};{ra_ucac};{dec_ucac};{mag_ucac};{abs(delta_a1)};{abs(delta_d1)}\n"
            out = out.replace('.', ',')

        thread_count += 1
        out_file.write(out)

    print(f"Complited. Total {thread_count} lines - Thread Id = {thread_id}")
    tycho_2_file.close()
    out_file.close()


def main():
    base.cw_start("Compare and Delta 1")
    base.cw("Starting a directory comparison")

    db = base.DBHConnection()

    cursor = db.cursor_execute("DROP TABLE IF EXISTS compare")
    cursor = db.cursor_execute("""CREATE TABLE `compare` ( `star_id` INT NOT NULL AUTO_INCREMENT , 
    `mean_ra_tycho` DOUBLE NOT NULL , `mean_dec_tycho` DOUBLE NOT NULL , 
    `mag_bt_tycho` DOUBLE NOT NULL ,`mag_vt_tycho` DOUBLE NOT NULL ,
     `mean_ra_ucac` DOUBLE NOT NULL , `mean_dec_ucac` DOUBLE NOT NULL , 
    `mag_ucac` DOUBLE NOT NULL ,`delta_a1` DOUBLE NULL ,`delta_d1` DOUBLE NULL ,
     UNIQUE `id` (`star_id`)) ENGINE = InnoDB;""")

    prc = []
    out_filenames = []
    for i in range(locations.process_count):
        out_filenames.append(locations.sql_out_filename_example + f"{i}" + ".txt")

    for i in range(locations.process_count):
        pr = Process(target=compare, args=(out_filenames[i], locations.tycho_txt_filename, i,))
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
        f"LOAD DATA INFILE '{locations.sql_out_compare_filename}' INTO TABLE compare FIELDS TERMINATED BY ';' (mean_ra_tycho,mean_dec_tycho,mag_bt_tycho,mag_vt_tycho,mean_ra_ucac,mean_dec_ucac,mag_ucac,delta_a1,delta_d1) SET star_id=NULL")
    cursor = db.cursor_execute(f"ALTER TABLE `compare` ADD INDEX `ra` (`mean_ra_tycho`);")
    cursor = db.cursor_execute(f"ALTER TABLE `compare` ADD INDEX `dec` (`mean_dec_tycho`);")

    base.cw("Finished loading database")
    base.cw_finish()


if __name__ == "__main__":
    main()
