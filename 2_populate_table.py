import sys
import pprint
import xlrd
from datetime import datetime
from config import db_connection


def main():
    conn = db_connection()
    cursor = conn.cursor()

    workbook = xlrd.open_workbook("./inventory_data.xls")

    worksheet = workbook.sheet_by_name('PACKING LIST')

    print ("Goint to print values")
    print (worksheet.cell(4, 1).value)
    sql = """INSERT INTO Inventory_data(inventory_code , barcode  ,reference_num  , name  , description  ,
            order_num  , receiving_date  , category  ,major_type  , sub_type  , item_type  , unit  , weight  , location  ,
            qty_ordered  , qty_delivered  , batch_number  , origin_location  ,carton_num  , box1_num  , box1_quantity  ,
            box2_num  ,  box2_quantity  , box3_num  , box3_quantity  ,box4_num  , box4_quantity  ,box5_num  ,box5_quantity, total_quantity_recieved  )
                     VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                          , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s)"""
    for i in range(worksheet.nrows ):
        inventory_code = worksheet.cell(i + 3, 0).value
        barcode = worksheet.cell(i + 3, 1).value
        reference_num = worksheet.cell(i + 3, 2).value
        name = worksheet.cell(i + 3, 3).value
        description = worksheet.cell(i + 3, 3).value
        order_num = worksheet.cell(i + 3, 4).value
        receiving_date = worksheet.cell(i + 3, 5).value
        category = worksheet.cell(i + 3, 6).value
        major_type = worksheet.cell(i + 3, 7).value
        sub_type = worksheet.cell(i + 3, 8).value
        item_type = worksheet.cell(i + 3, 9).value
        unit = worksheet.cell(i + 3, 10).value
        weight = str(worksheet.cell(i + 3, 11).value)
        location = worksheet.cell(i + 3, 12).value
        qty_ordered = worksheet.cell(i + 3, 13).value
        qty_delivered = worksheet.cell(i + 3, 14).value
        batch_number = worksheet.cell(i + 3, 15).value
        origin_location = str(worksheet.cell(i + 3, 16).value)
        carton_num = worksheet.cell(i + 3, 17).value
        box1_num = worksheet.cell(i + 3, 19).value
        box1_quantity = str(worksheet.cell(i + 3, 20).value)
        box2_num = str(worksheet.cell(i + 3, 21).value)
        box2_quantity = str(worksheet.cell(i + 3, 22).value)
        box3_num = str(worksheet.cell(i + 3, 23).value)
        box3_quantity = str(worksheet.cell(i + 3, 24).value)
        box4_num = str(worksheet.cell(i + 3, 25).value)
        box4_quantity = str(worksheet.cell(i + 3, 26).value)
        box5_num = str(worksheet.cell(i + 3, 27).value)
        box5_quantity = worksheet.cell(i + 3, 28).value
        total_quantity_recieved = worksheet.cell(i + 3, 29).value

        values = (inventory_code, barcode, reference_num, name, description,
                  order_num, receiving_date, category, major_type, sub_type, item_type, unit, weight, location,
                  qty_ordered, qty_delivered, batch_number, origin_location, carton_num, box1_num, box1_quantity,
                  box2_num, box2_quantity, box3_num, box3_quantity, box4_num, box4_quantity, box5_num, box5_quantity,
                  total_quantity_recieved)
        cursor.execute(sql, values)
        conn.commit()

    print ("Data added to Table")



if __name__ == "__main__":
    main()


