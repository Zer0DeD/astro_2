# calculating delta 4


import base
import locations
import io


def main():
    base.cw_start("Delta 4")
    db = base.DBHConnection()

    cursor = db.cursor_execute("DROP TABLE IF EXISTS delta_4")

    cursor = db.cursor_execute("""CREATE TABLE `delta_4` ( `star_id` INT NOT NULL AUTO_INCREMENT , 
        `delta_a4` DOUBLE NOT NULL , `delta_d4` DOUBLE NOT NULL , `compare_id` INT NOT NULL , UNIQUE `id` (`star_id`)) ENGINE = InnoDB;""")

    base.cw("Start creating Delta 4 file")

    out_file = io.open(locations.sql_out_delta4_filename, "w", newline='\n')

    for grad in range(-90, 90):
        if grad % 30 == 0:
            print(f"Complited {grad} (-90, 90)")

        cursor = db.cursor_execute(f"""SELECT star_id FROM compare 
                        WHERE mean_dec_tycho >= {grad} AND mean_dec_tycho < {grad + 1}""")

        if cursor.rowcount <= 1:
            continue

        star_id_t = cursor.fetchall()
        star_id_arr = []

        for i in range(0, len(star_id_t)):
            star_id_arr.append(star_id_t[i][0])

        sum_delta_a3 = 0
        sum_delta_d3 = 0

        for i in range(0, len(star_id_arr)):
            cursor = db.cursor_execute(f"SELECT delta_a3, delta_d3 FROM delta_3 WHERE compare_id = {star_id_arr[i]}")
            data = cursor.fetchone()
            sum_delta_d3 += data[1]
            sum_delta_a3 += data[0]

        delta_d = sum_delta_d3 / len(star_id_arr)

        for i in range(0, len(star_id_arr)):
            star_id = star_id_arr[i]

            cursor = db.cursor_execute(f"SELECT delta_a3, delta_d3 FROM delta_3 WHERE compare_id = {star_id}")
            delta = cursor.fetchone()

            delta_a4 = delta[0]
            delta_d4 = delta[1] - delta_d

            if locations._en:
                out = f"{abs(delta_a4)};{abs(delta_d4)};{star_id}\n"
            else:
                out = f"{abs(delta_a4)};{abs(delta_d4)};{star_id}\n"
                out = out.replace('.', ',')
            out_file.write(out)

    out_file.close()

    base.cw("Finished creating Delta 4 file")
    base.cw("Start loading database")

    cursor = db.cursor_execute(
        f"LOAD DATA INFILE '{locations.sql_out_delta4_filename}' INTO TABLE delta_4 FIELDS TERMINATED BY ';' (delta_a4, delta_d4, compare_id) SET star_id=NULL")

    cursor = db.cursor_execute("ALTER TABLE `delta_4` ADD INDEX `id_com4` (`compare_id`);")

    base.cw("Finished loading database")
    base.cw_finish()


if __name__ == "__main__":
    main()
