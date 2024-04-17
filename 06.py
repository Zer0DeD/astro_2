# calculating delta 5


import base
import locations
import io


def main():
    base.cw_start("Delta 5")
    db = base.DBHConnection()
    cursor = db.cursor_execute("DROP TABLE IF EXISTS delta_5")
    cursor = db.cursor_execute("""CREATE TABLE `delta_5` ( `star_id` INT NOT NULL AUTO_INCREMENT , 
        `delta_a5` DOUBLE NOT NULL , `delta_d5` DOUBLE NOT NULL , `compare_id` INT NOT NULL , UNIQUE `id` (`star_id`)) ENGINE = InnoDB;""")

    base.cw("Start creating Delta 5 file")
    out_file = io.open(locations.sql_out_delta5_filename, "w", newline='\n')

    for mag in range(-20, 20):
        if mag % 10 == 0:
            print(f"Complited {mag} (-20, 20)")

        cursor = db.cursor_execute(
            f"SELECT star_id FROM compare WHERE mag_bt_tycho >= {mag} AND mag_bt_tycho < {mag + 1}")

        if cursor.rowcount < 1:
            continue

        star_id_t = cursor.fetchall()
        star_id_arr = []

        for i in range(0, len(star_id_t)):
            star_id_arr.append(star_id_t[i][0])

        sum_delta_a4 = 0
        sum_delta_d4 = 0

        for i in range(0, len(star_id_arr)):
            cursor = db.cursor_execute(f"SELECT delta_a4, delta_d4 FROM delta_4 WHERE compare_id = {star_id_arr[i]}")

            sum_delta = cursor.fetchone()
            sum_delta_a4 += sum_delta[0]
            sum_delta_d4 += sum_delta[1]

        delta_a = sum_delta_a4 / len(star_id_arr)
        delta_d = sum_delta_d4 / len(star_id_arr)

        for i in range(0, len(star_id_arr)):
            star_id = star_id_arr[i]

            cursor = db.cursor_execute(f"SELECT delta_a4, delta_d4 FROM delta_4 WHERE compare_id = {star_id}")
            delta = cursor.fetchone()

            delta_a5 = delta[0] - delta_a
            delta_d5 = delta[1] - delta_d

            if locations._en:
                out = f"{abs(delta_a5)};{abs(delta_d5)};{star_id}\n"
            else:
                out = f"{abs(delta_a5)};{abs(delta_d5)};{star_id}\n"
                out = out.replace('.', ',')
            out_file.write(out)

    out_file.close()
    base.cw("Finished creating Delta 5 file")
    base.cw("Start loading database")

    cursor = db.cursor_execute(
        f"LOAD DATA INFILE '{locations.sql_out_delta5_filename}' INTO TABLE delta_5 FIELDS TERMINATED BY ';' (delta_a5, delta_d5, compare_id) SET star_id=NULL")

    cursor = db.cursor_execute("ALTER TABLE `delta_5` ADD INDEX `id_com5` (`compare_id`);")

    base.cw("Finished loading database")
    base.cw_finish()


if __name__ == "__main__":
    main()
