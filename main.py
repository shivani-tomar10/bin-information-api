import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector

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


# Request model for finding/deleting a BIN
class BinRequest(BaseModel):
    bin_iin: str


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


# Request model for creating/updating a BIN
class BinCreateRequest(BaseModel):
    bin_iin: str
    network: str
    card_type: str
    card_category: str
    issuer: str


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