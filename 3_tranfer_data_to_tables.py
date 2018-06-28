import sys
import pprint
import xlrd
from datetime import datetime
from config import db_connection

def main():
    conn = db_connection()
    cursor = conn.cursor()

    # Transfering data to real tables

    query = "Select * from inventory_data"
    cursor.execute(query)

    rows = cursor.fetchall()
    for row in rows:

        inventory_code = row[1]
        barcode = int(float(row[2]))
        reference_num = row[3]
        name = row[4]
        name = name.replace("'", "")
        name = str(name).strip()
        description = row[5]
        description = description.replace("'", "")
        order_num = row[6]
        receiving_date = row[7]
        receiving_date = datetime.strptime(receiving_date, '%d-%m-%Y').strftime('%Y-%m-%d')
        category = row[8]
        if (category == "Consmer"):
            category = "CO"
        elif (category == "Usable"):
            category = "US"
        else:
            category = ""

        major_type = row[9].upper()
        sub_type = row[10].upper()
        item_type = row[11]

        if (item_type == "For Sale"):
            item_type = "FS"
        elif (item_type == "Not For Sale"):
            item_type = "NFS"
        else:
            item_type = ""

        unit = row[12]
        weight = str(row[13])
        if (weight == ''):
            weight = '0'
        location = row[14]
        qty_ordered = row[15]
        qty_delivered = row[16]
        batch_number = row[17]
        origin_location = str(row[18])
        carton_num = row[19]
        box1_num = row[20]
        box1_quantity = str(row[21])
        box2_num = str(row[22])
        box2_quantity = str(row[23])
        box3_num = str(row[24])
        box3_quantity = str(row[25])
        box4_num = str(row[26])
        box4_quantity = str(row[27])
        box5_num = str(row[28])
        box5_quantity = row[29]
        total_quantity_recieved = row[30]
        total_quantity_recieved = int(float(total_quantity_recieved))
        print ("type: ", type(row[30]))
        # Major Type
        major_type_query = """SELECT * FROM inventory_productmajortype WHERE UPPER(name)='%s' """ % major_type
        cursor.execute(major_type_query)
        majortypes = cursor.fetchall()
        majortype_obj = None

        if (len(majortypes) > 0):  # already exists
            majortype_obj = majortypes[0][0]
            print("major type already exists as %s with id: %s" % (major_type, majortype_obj))
        else:  # else dont exist so add new
            major_type_insertion = """INSERT INTO inventory_productmajortype(name) VALUES('%s') """ % major_type
            cursor.execute(major_type_insertion)
            conn.commit()
            major_type_query = """SELECT * FROM inventory_productmajortype WHERE UPPER(name)='%s' """ % major_type
            cursor.execute(major_type_query)
            majortypes = cursor.fetchall()
            majortype_obj = majortypes[0][0]
            # print("added new major type as %s with id = " % (major_type, majortype_obj))


            # Product brand
        #             Not available in excel sheet

        #         Sub Type
        sub_type_query = """SELECT * FROM inventory_productsubtype WHERE UPPER(name)='%s' """ % sub_type
        cursor.execute(sub_type_query)
        subtypes = cursor.fetchall()
        subtype_obj = None
        if (len(subtypes) > 0):  # subtype already exists
            subtype_obj = subtypes[0][0]
            major_sub_query = """SELECT * FROM inventory_productsubtype_major_type WHERE productsubtype_id='%s' and productmajortype_id='%s' """ % (
                subtype_obj, majortype_obj)
            cursor.execute(major_sub_query)
            result = cursor.fetchall()
            if (len(result) > 0):  # if inventory relation exist
                pass
            else:
                insertion_query = """INSERT INTO inventory_productsubtype_major_type( productsubtype_id,productmajortype_id) VALUES('%s','%s') """ % (
                    subtype_obj, majortype_obj)
                cursor.execute(insertion_query)
                conn.commit()
            print(result)
        else:  # sub type does not exist
            sub_type_insertion = """INSERT INTO inventory_productsubtype(name) VALUES('%s') """ % sub_type
            cursor.execute(sub_type_insertion)
            conn.commit()
            sub_type_query = """SELECT * FROM inventory_productsubtype WHERE UPPER(name)='%s' """ % sub_type
            cursor.execute(sub_type_query)
            subtypes = cursor.fetchall()
            subtype_obj = subtypes[0][0]

            major_sub_query = """SELECT * FROM inventory_productsubtype_major_type WHERE productsubtype_id='%s' and productmajortype_id='%s' """ % (
                subtype_obj, majortype_obj)
            cursor.execute(major_sub_query)
            result = cursor.fetchall()
            if (len(result) > 0):  # if inventory relation exist
                pass
            else:
                insertion_query = """INSERT INTO inventory_productsubtype_major_type( productsubtype_id,productmajortype_id) VALUES('%s','%s') """ % (
                    subtype_obj, majortype_obj)
                cursor.execute(insertion_query)
                conn.commit()
        try:
            insert_inventory_query = """INSERT INTO inventory_inventory( inventory_code, major_type_id, sub_type_id) VALUES('%s' ,'%s','%s') """ % (
                inventory_code, majortype_obj, subtype_obj)
            cursor.execute(insert_inventory_query)
            conn.commit()
        except:
            cursor.close()
            conn.close()
            try:
                conn = db_connection()
            except:
                print ("Unable to connect to database")
            cursor = conn.cursor()
            continue
        get_inventory_query = """SELECT * FROM inventory_inventory WHERE inventory_code='%s' and major_type_id='%s' and sub_type_id='%s' """ % (
            inventory_code, majortype_obj, subtype_obj)
        cursor.execute(get_inventory_query)
        inventory = cursor.fetchall()
        inventory_obj = inventory[0][0]
        print(inventory)
        try:
            insert_product_query = """INSERT INTO inventory_product( product_name, weight, weight_unit, barcode,
                item_type, item_category, quantity, receiving_date, description, inventory_product_id , reference_number
                ) VALUES('%s' ,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') """ % (
                name, weight, unit, barcode, item_type, category, total_quantity_recieved, receiving_date, description,
                inventory_obj, reference_num)
            cursor.execute(insert_product_query)
            conn.commit()
        except:
            cursor.close()
            conn.close()
            try:
                conn = db_connection()
            except:
                print ("Unable to connect to database")
            cursor = conn.cursor()
            continue
        get_inventory_product = """SELECT * FROM inventory_product WHERE inventory_product_id='%s' """ % (
            inventory_obj)
        cursor.execute(get_inventory_product)
        inventory_product = cursor.fetchall()
        inventory_product_obj = inventory_product[0][0]

        insert_product_query = """INSERT INTO inventory_productlocation( location, quantity, product_id )
                                  VALUES('%s' ,'%s','%s') """ % ('SL', 0, inventory_product_obj)
        cursor.execute(insert_product_query)
        conn.commit()
        insert_product_query = """INSERT INTO inventory_productlocation( location, quantity, product_id )
                                          VALUES('%s' ,'%s','%s') """ % (
            'IU', 0, inventory_product_obj)
        cursor.execute(insert_product_query)
        conn.commit()
        insert_product_query = """INSERT INTO inventory_productlocation( location, quantity, product_id )
                                          VALUES('%s' ,'%s','%s') """ % (
            'WH', total_quantity_recieved , inventory_product_obj)
        cursor.execute(insert_product_query)
        conn.commit()




        insert_product_query = """INSERT INTO inventory_productstatus( status, quantity, product_id )
                                                  VALUES('%s' ,'%s','%s') """ % (
            'WS', 0, inventory_product_obj)
        cursor.execute(insert_product_query)
        conn.commit()

        insert_product_query = """INSERT INTO inventory_productstatus( status, quantity, product_id )
                                                          VALUES('%s' ,'%s','%s') """ % (
            'SP', 0, inventory_product_obj)
        cursor.execute(insert_product_query)
        conn.commit()

        insert_product_query = """INSERT INTO inventory_productstatus( status, quantity, product_id )
                                                          VALUES('%s' ,'%s','%s') """ % (
            'EX', 0, inventory_product_obj)
        cursor.execute(insert_product_query)
        conn.commit()


if __name__ == "__main__":
    main()















