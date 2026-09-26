import os
from dotenv import load_dotenv
from fastapi import FastAPI
import mysql.connector
from module import BinRequest, BinCreateRequest, SuggestionRequest


app = FastAPI()
load_dotenv()


# MySQL connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("MYSQL_PASSWORD"),
    database="bin_database"
)

cursor = connection.cursor()


# GET/FIND BIN
@app.post("/bin")
def get_bin(data: BinRequest):

    cursor.execute(
        "SELECT * FROM bin_data WHERE bin_iin = %s",
        (data.bin_iin,)
    )

    row = cursor.fetchone()

    if row is None:
        return {"message": "BIN not found"}

    return {"data": row}


# CREATE BIN
@app.post("/bin/create")
def create_bin(data: BinCreateRequest):

    cursor.execute(
        """
        INSERT INTO bin_data
        (bin_iin, network, card_type, card_category, issuer)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            data.bin_iin,
            data.network,
            data.card_type,
            data.card_category,
            data.issuer
        )
    )

    connection.commit()

    return {"message": "BIN created successfully"}


# UPDATE BIN
@app.put("/bin/update")
def update_bin(data: BinCreateRequest):

    cursor.execute(
        """
        UPDATE bin_data
        SET network = %s,
            card_type = %s,
            card_category = %s,
            issuer = %s
        WHERE bin_iin = %s
        """,
        (
            data.network,
            data.card_type,
            data.card_category,
            data.issuer,
            data.bin_iin
        )
    )

    connection.commit()

    if cursor.rowcount == 0:
        return {"message": "BIN not found"}

    return {"message": "BIN updated successfully"}


# DELETE BIN
@app.delete("/bin/delete")
def delete_bin(data: BinRequest):

    cursor.execute(
        "DELETE FROM bin_data WHERE bin_iin = %s",
        (data.bin_iin,)
    )

    connection.commit()

    if cursor.rowcount == 0:
        return {"message": "BIN not found"}

    return {"message": "BIN deleted successfully"}

# AUTO SUGGESTION
@app.post("/bin/suggest")
def suggest_bin(data: SuggestionRequest):

    search = data.query.strip()

    if not search:
        return {"suggestions": []}

    search = f"%{search}%"

    cursor.execute(
        """
        SELECT *
        FROM bin_data
        WHERE bin_iin LIKE %s
           OR network LIKE %s
           OR card_category LIKE %s
           OR issuer LIKE %s
        LIMIT 10
        """,
        (
            search,
            search,
            search,
            search
        )
    )

    rows = cursor.fetchall()

    return {
        "suggestions": [
            {
                "id": row[0],
                "bin_iin": row[1],
                "network": row[2],
                "card_type": row[3],
                "card_category": row[4],
                "issuer": row[5]
            }
            for row in rows
        ]
    }
