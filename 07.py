# calculating delta 6


import base
import locations
import io


def delta_6(left, rigth, db, out_file):
    cursor = db.cursor_execute(
        f"SELECT star_id FROM compare WHERE (mag_bt_tycho - mag_vt_tycho) > {left} AND (mag_bt_tycho - mag_vt_tycho) <= {rigth}")

    if cursor.rowcount <= 1:
        return

    star_id_t = cursor.fetchall()
    star_id_arr = []

    for i in range(0, len(star_id_t)):
        star_id_arr.append(star_id_t[i][0])

    sum_delta_a5 = 0
    sum_delta_d5 = 0

    for i in range(0, len(star_id_arr)):
        star_id = star_id_arr[i]

        cursor = db.cursor_execute(f"SELECT delta_a5, delta_d5 FROM delta_5 WHERE compare_id = {star_id}")

        if cursor.rowcount == 0:
            print(star_id)
            continue

        sum_delta = cursor.fetchone()
        sum_delta_a5 += sum_delta[0]
        sum_delta_d5 += sum_delta[1]

    delta_a = sum_delta_a5 / len(star_id_arr)
    delta_d = sum_delta_d5 / len(star_id_arr)

    for i in range(0, len(star_id_arr)):
        star_id = star_id_arr[i]

        cursor = db.cursor_execute(f"SELECT delta_a5, delta_d5 FROM delta_5 WHERE compare_id = {star_id}")

        if cursor.rowcount == 0:
            continue

        delta = cursor.fetchone()
        delta_a6 = delta[0] - delta_a
        delta_d6 = delta[1] - delta_d

        if locations._en:
            out = f"{abs(delta_a6)};{abs(delta_d6)};{star_id}\n"
        else:
            out = f"{abs(delta_a6)};{abs(delta_d6)};{star_id}\n"
            out = out.replace('.', ',')
        out_file.write(out)


def main():
    base.cw_start("Delta 6")
    db = base.DBHConnection()

    cursor = db.cursor_execute("DROP TABLE IF EXISTS delta_6")

    cursor = db.cursor_execute("""CREATE TABLE `delta_6` ( `star_id` INT NOT NULL AUTO_INCREMENT , 
        `delta_a6` DOUBLE NOT NULL , `delta_d6` DOUBLE NOT NULL , `compare_id` INT NOT NULL , UNIQUE `id` (`star_id`)) ENGINE = InnoDB;""")

    base.cw("Start creating Delta 6 file")

    out_file = io.open(locations.sql_out_delta6_filename, "w", newline='\n')

    ########    O (-00;-0,4]
    delta_6(-100, -0.4, db, out_file)

    base.cw("O Complited")

    ########    B (-0.4;0]
    delta_6(-0.4, 0, db, out_file)

    base.cw("B Complited")

    ########    A (0;0.4]
    delta_6(0, 0.4, db, out_file)

    base.cw("A Complited")

    ########    F (0.4;0.6]
    delta_6(0.4, 0.6, db, out_file)

    base.cw("F Complited")

    ########    G (0.6;0.8]
    delta_6(0.6, 0.8, db, out_file)

    base.cw("G Complited")

    ########    K (0.8;1.4]
    delta_6(0.8, 1.4, db, out_file)

    base.cw("K Complited")

    ########    M (1.4;+00]
    delta_6(1.4, 100, db, out_file)

    base.cw("M Complited")
    out_file.close()

    base.cw("Start loading database")

    cursor = db.cursor_execute(
        f"LOAD DATA INFILE '{locations.sql_out_delta6_filename}' INTO TABLE delta_6 FIELDS TERMINATED BY ';' (delta_a6, delta_d6, compare_id) SET star_id=NULL")

    cursor.execute("ALTER TABLE `delta_6` ADD INDEX `id_com6` (`compare_id`);")

    base.cw("Finished loading database")
    base.cw_finish()


if __name__ == "__main__":
    main()
