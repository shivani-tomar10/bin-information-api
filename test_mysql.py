import os
from dotenv import load_dotenv
import mysql.connector
import csv

load_dotenv()


# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("MYSQL_PASSWORD"),
    database="bin_database"
)

print("MySQL connected:", connection.is_connected())

cursor = connection.cursor()


# Open CSV file
with open("bin_data.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        cursor.execute(
            """
            INSERT INTO bin_data
            (bin_iin, network, card_type, card_category, issuer)
            SELECT %s, %s, %s, %s, %s
            WHERE NOT EXISTS (
                SELECT 1 FROM bin_data WHERE bin_iin = %s
            )
            """,
            (
                row["BIN/IIN"],
                row["Network/Scheme"],
                row["Card Type"],
                row["Card Category"],
                row["Issuer"],
                row["BIN/IIN"]
            )
        )


# Save changes
connection.commit()

print("CSV data inserted successfully!")


# Close connection
cursor.close()
connection.close()

print("MySQL connection closed.")