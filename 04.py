# calculating delta 3


import base
import locations
import io


def main():
    base.cw_start("Delta 3")
    db = base.DBHConnection()
    cursor = db.cursor_execute("DROP TABLE IF EXISTS delta_3")

    cursor = db.cursor_execute("""CREATE TABLE `delta_3` ( `star_id` INT NOT NULL AUTO_INCREMENT , 
        `delta_a3` DOUBLE NOT NULL , `delta_d3` DOUBLE NOT NULL , `compare_id` INT NOT NULL , UNIQUE `id` (`star_id`)) ENGINE = InnoDB;""")

    base.cw("Start creating Delta 3 file")
    out_file = io.open(locations.sql_out_delta3_filename, 'w', newline='\n')
    for grad in range(0, 360):
        if grad % 30 == 0:
            print(f"Complited {grad} (0, 360)")

        cursor = db.cursor_execute(f"""SELECT star_id FROM compare 
                        WHERE mean_ra_tycho >= {grad} AND mean_ra_tycho < {grad + 1}""")

        if cursor.rowcount <= 1:
            continue

        star_id_t = cursor.fetchall()
        star_id_arr = []

        for i in range(0, len(star_id_t)):
            star_id_arr.append(star_id_t[i][0])

        sum_delta_a2 = 0
        sum_delta_d2 = 0

        for i in range(0, len(star_id_arr)):
            cursor = db.cursor_execute(f"SELECT delta_a2 FROM delta_2 WHERE compare_id = {star_id_arr[i]}")
            data = cursor.fetchone()
            sum_delta_a2 += data[0]
            sum_delta_d2 += data[0]

        delta_a = sum_delta_a2 / len(star_id_arr)
        delta_d = sum_delta_d2 / len(star_id_arr)

        for i in range(0, len(star_id_arr)):
            star_id = star_id_arr[i]

            cursor = db.cursor_execute(f"SELECT delta_a2, delta_d2 FROM delta_2 WHERE compare_id = {star_id}")
            delta = cursor.fetchone()

            delta_a3 = delta[0] - delta_a
            delta_d3 = delta[1] - delta_d

            if locations._en:
                out = f"{abs(delta_a3)};{abs(delta_d3)};{star_id}\n"
            else:
                out = f"{abs(delta_a3)};{abs(delta_d3)};{star_id}\n"
                out = out.replace('.', ',')
            out_file.write(out)

    out_file.close()

    base.cw("Finished creating Delta 3 file")
    base.cw("Start loading database")

    cursor.execute(
        f"LOAD DATA INFILE '{locations.sql_out_delta3_filename}' INTO TABLE delta_3 FIELDS TERMINATED BY ';' (delta_a3, delta_d3, compare_id) SET star_id=NULL")

    cursor.execute("ALTER TABLE `delta_3` ADD INDEX `id_com3` (`compare_id`);")

    base.cw("Finished loading database")
    base.cw_finish()


if __name__ == "__main__":
    main()
