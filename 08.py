# final answer


import base
import locations
import re


def main():
    base.cw_start("Final answer")
    db = base.DBHConnection()

    cursor = db.cursor_execute("SELECT count(1) FROM delta_6")
    count = cursor.fetchone()[0]

    cursor = db.cursor_execute("SELECT sum(delta_a6) FROM delta_6")

    sum_delta_a6 = cursor.fetchone()[0]
    delta_a = sum_delta_a6 / count

    cursor = db.cursor_execute("SELECT sum(delta_d6) FROM delta_6")

    sum_delta_d6 = cursor.fetchone()[0]
    delta_d = sum_delta_d6 / count

    print(f"Delta a = {delta_a * 3600} sec;\nDelta d = {delta_d * 3600} sec;\nN = {count}")

    file = open(locations.sql_out_answers_filename, 'w')
    if locations._en:
        out = f"Delta a = {delta_a * 3600} sec;\nDelta d = {delta_d * 3600} sec;\nN = {count}"
    else:
        out = f"Delta a = {delta_a * 3600} sec;\nDelta d = {delta_d * 3600} sec;\nN = {count}"
        out = out.replace('.', ',')
    file.write(out)
    file.close()

    base.cw_finish()


if __name__ == "__main__":
    main()
