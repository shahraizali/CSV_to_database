import psycopg2
import sys
import pprint
import xlrd
from datetime import datetime
from config import db_connection


def main():
    conn = db_connection()
    cursor = conn.cursor()

    # Creating table with name Inventory_data

    creating_table = """
          CREATE TABLE Inventory_data (
            id SERIAL PRIMARY KEY,
            inventory_code VARCHAR(255)   NULL,
            barcode VARCHAR(255)   NULL,
            reference_num VARCHAR(255)   NULL,
            name VARCHAR(255)   NULL,
            description VARCHAR(255)   NULL,
            order_num VARCHAR(255)   NULL,
            receiving_date VARCHAR(255)   NULL,
            category VARCHAR(255)   NULL,
            major_type VARCHAR(255)   NULL,
            sub_type VARCHAR(255)   NULL,
            item_type VARCHAR(255)   NULL,
            unit VARCHAR(255)   NULL,
            weight VARCHAR(255)   NULL,
            location VARCHAR(255)   NULL,
            qty_ordered VARCHAR(255)   NULL,
            qty_delivered VARCHAR(255)   NULL,
            batch_number VARCHAR(255)   NULL,
            origin_location VARCHAR(255)   NULL,
            carton_num VARCHAR(255)   NULL,

            box1_num VARCHAR(255)   NULL,
            box1_quantity VARCHAR(255)   NULL,

            box2_num VARCHAR(255)   NULL,
            box2_quantity VARCHAR(255)   NULL,

            box3_num VARCHAR(255)   NULL,
            box3_quantity VARCHAR(255)   NULL,

            box4_num VARCHAR(255)   NULL,
            box4_quantity VARCHAR(255)   NULL,

            box5_num VARCHAR(255)   NULL,
            box5_quantity VARCHAR(255)   NULL,
            total_quantity_recieved VARCHAR(255)   NULL
        )"""

    cursor.execute(creating_table)

    conn.commit()

    print("Created Table")


if __name__ == "__main__":
    main()