from connection import ims_db_dept_cursor, ims_cursor, ims_db_dept, ims_db_gh
from utils import out
from time import sleep

from datetime import datetime

ims_cursor.execute(
    "SELECT name, qty FROM products")

for item in ims_cursor.fetchall():

    # for each stock in products where the stock is in feed_datatable
    # check if it's the same day
    # if datetime timezone gmt is morning, execute morning value else night values
    #   if true :
    #     update
    #   else insert new date
        
    ims_db_dept_cursor.execute(
        f"SELECT date, stock_name FROM `feed_datatable` WHERE stock_name = '{item[0]}'"
    )
    is_same_day = [row_data[0].date() == datetime.today().date() for row_data in ims_db_dept_cursor] or False
    # TODO ::: check timezone
    # out(is_same_day)
    is_day = True
    is_night = False
    
    if is_day:
        if is_same_day:
            out("same day")
            ims_db_dept_cursor.execute(
                f"UPDATE `feed_datatable` SET `day`='5' WHERE stock_name='{item[0]}'"
            )
        else:    
            out("new day")
            ims_db_dept_cursor.execute(
                f"INSERT INTO `feed_datatable`(`stock_name`, `day`, `night`, `used`, `available`) VALUES ('{item[0]}','46','0','80','{item[1]}')"
            )
    # if is_night:
ims_db_dept.commit()
out("done")





# CREATE TABLE `ims_db_dept_gh`. ( `id` INT(255) NOT NULL AUTO_INCREMENT , `date` DATETIME(255) NOT NULL DEFAULT CURRENT_TIMESTAMP , `day` INT(255) NOT NULL , `night` INT(255) NOT NULL , `used` INT(255) NOT NULL , `available` INT(255) NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;

# INSERT INTO `feed_datatable`(`day`, `night`, `used`, `available`) VALUES ('46','36','80','400')
