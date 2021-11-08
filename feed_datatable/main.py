from connection import ims_db_dept_cursor, ims_cursor, ims_db_dept, ims_db_gh
from utils import out
from time import sleep
from datetime import datetime
import sys

ims_cursor.execute(
    "SELECT name, qty FROM products")

is_day = sys.argv[1]=="day"
is_night = sys.argv[1]=="night"

for item in ims_cursor.fetchall():

    is_same_day=None
    ims_db_dept_cursor.execute(
        f"SELECT date, stock_name FROM `feed_datatable` WHERE stock_name = '{item[0]}'"
    )
    for row_data in ims_db_dept_cursor:
        if row_data[0].date() == datetime.today().date():
            is_same_day=True

    if is_day:
        if is_same_day:
            out("same day")

            latest_row = ims_db_dept_cursor.execute(
                f"SELECT * FROM `feed_datatable` WHERE stock_name = '{item[0]}' ORDER BY id DESC LIMIT 1;"
            )

            initial_stock_row = ims_db_dept_cursor.fetchone()
            initial_stock_id = initial_stock_row[0]
            initial_stock_available = initial_stock_row[-1]
            initial_stock_used = initial_stock_row[-2]
            final_stock_available = int(item[1])
            used_stock = initial_stock_available - final_stock_available
            used_stock = initial_stock_used + used_stock

            ims_db_dept_cursor.execute(
                f"UPDATE `feed_datatable` SET `day`='{used_stock}' ,`used`='{used_stock}' WHERE stock_name='{item[0]}' AND id='{initial_stock_id}';"
            )

            # out(initial_stock_row)

        else:
            out("new day")
            ims_db_dept_cursor.execute(
                f"INSERT INTO `feed_datatable`(`stock_name`, `day`, `night`, `used`, `available`) VALUES ('{item[0]}','0','0','0','{item[1]}')"
            )

    if is_night:
        if is_same_day:
            out("same day")

            latest_row = ims_db_dept_cursor.execute(
                f"SELECT * FROM `feed_datatable` WHERE stock_name = '{item[0]}' ORDER BY id DESC LIMIT 1;"
            )

            initial_stock_row = ims_db_dept_cursor.fetchone()
            initial_stock_id = initial_stock_row[0]
            initial_stock_available = initial_stock_row[-1]
            day_stock_used = initial_stock_row[3]
            final_stock_available = int(item[1])
            used_stock = initial_stock_available - final_stock_available - day_stock_used
            final_used_stock = initial_stock_available - final_stock_available

            ims_db_dept_cursor.execute(
                f"UPDATE `feed_datatable` SET `night`='{used_stock}' ,`used`='{final_used_stock}' WHERE stock_name='{item[0]}' AND id='{initial_stock_id}';"
            )
        else:
            out("new day")
            ims_db_dept_cursor.execute(
                f"INSERT INTO `feed_datatable`(`stock_name`, `day`, `night`, `used`, `available`) VALUES ('{item[0]}','0','0','0','{item[1]}')"
            )

ims_db_dept.commit()
out("done")
