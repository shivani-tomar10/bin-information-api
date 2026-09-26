import os
import csv
from dotenv import load_dotenv
import mysql.connector


load_dotenv()

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("MYSQL_PASSWORD"),
    database="bin_database"
)

cursor = connection.cursor()

print("MySQL connected:", connection.is_connected())


with open("bin_data_v2.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    query = """
        INSERT INTO bin_data
        (bin_iin, network, card_type, card_category, issuer)
        VALUES (%s, %s, %s, %s, %s)
    """

    batch = []

    for row in reader:

        batch.append((
            row["BIN/IIN"],
            row["Network/Scheme"],
            row["Card Type"],
            row["Card Category"],
            row["Issuer"]
        ))

        if len(batch) == 1000:

            cursor.executemany(query, batch)
            connection.commit()

            batch.clear()

            print("1000 records inserted")


    if batch:

        cursor.executemany(query, batch)
        connection.commit()


print("CSV data inserted successfully!")


cursor.close()
connection.close()

print("MySQL connection closed.")