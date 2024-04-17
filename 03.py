# calculating delta 2


import base
import locations
import io


def main():
    base.cw_start("Delta 2")
    db = base.DBHConnection()

    cursor = db.cursor_execute("DROP TABLE IF EXISTS delta_2")
    cursor = db.cursor_execute("""CREATE TABLE `delta_2` ( `star_id` INT NOT NULL AUTO_INCREMENT , 
    `delta_a2` DOUBLE NOT NULL , `delta_d2` DOUBLE NOT NULL , `compare_id` INT NOT NULL , UNIQUE `id` (`star_id`)) ENGINE = InnoDB;""")

    cursor = db.cursor_execute("SELECT count(1) FROM compare")
    count = cursor.fetchone()[0]

    cursor = db.cursor_execute("SELECT sum(delta_a1) FROM compare")
    sum_delta_a1 = cursor.fetchone()[0]

    A = sum_delta_a1 / count

    cursor = db.cursor_execute("SELECT sum(delta_d1) FROM compare")
    sum_delta_d1 = cursor.fetchone()[0]

    D = sum_delta_d1 / count

    cursor = db.cursor_execute("SELECT delta_a1, delta_d1, star_id FROM compare")
    my_t = cursor.fetchall()

    my_arr = []
    for i in range(0, len(my_t)):
        my_arr.append(list(my_t[i]))

    for i in range(0, len(my_arr)):
        my_arr[i][0] = my_arr[i][0] - A
        my_arr[i][1] = my_arr[i][1] - D

    base.cw("Start creating Delta 2 file")
    out_file = io.open(locations.sql_out_delta2_filename, "w", newline='\n')
    for i in range(0, len(my_arr)):
        if i % 200000 == 0:
            print(f"Complited {i} lines")
        if locations._en:
            out = f"{abs(my_arr[i][0])};{abs(my_arr[i][1])};{my_arr[i][2]}\n"
        else:
            out = f"{abs(my_arr[i][0])};{abs(my_arr[i][1])};{my_arr[i][2]}\n"
            out = out.replace('.', ',')
        out_file.write(out)
    print(f"Complited. Total {len(my_arr)} lines")
    out_file.close()

    base.cw("Finished creating Delta 2 file")
    base.cw("Start loading database")
    cursor = db.cursor_execute(
        f"LOAD DATA INFILE '{locations.sql_out_delta2_filename}' INTO TABLE delta_2 FIELDS TERMINATED BY ';' (delta_a2, delta_d2, compare_id) SET star_id=NULL")

    cursor = db.cursor_execute("ALTER TABLE `delta_2` ADD INDEX `id_com` (`compare_id`);")
    base.cw("Finished loading database")
    base.cw_finish()


if __name__ == "__main__":
    main()
