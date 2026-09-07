
import requests
import csv
from bs4 import BeautifulSoup
import mysql.connector


# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="shivi7890@",
    database="bin_database"
)

cursor = connection.cursor()

print("MySQL connected:", connection.is_connected())


# Store scraped data
data = []


# Scrape all pages
for page in range(1, 1999):

    print(f"Scraping page {page}")

    url = f"https://bintable.com/scheme/mastercard?page={page}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table")

        if not table:
            print(f"No table found on page {page}")
            continue

        rows = table.find_all("tr")

        for row in rows[1:]:

            cells = row.find_all("td")

            if len(cells) != 5:
                continue

            bin_iin = cells[0].text.strip()
            network = cells[1].text.strip()
            card_type = cells[2].text.strip()
            card_category = cells[3].text.strip()
            issuer = cells[4].text.strip()

            data.append([
                bin_iin,
                network,
                card_type,
                card_category,
                issuer
            ])

    except requests.RequestException as e:

        print(f"Error on page {page}: {e}")


print("Total records:", len(data))


# Save data into CSV
with open("bin_data.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "BIN/IIN",
        "Network/Scheme",
        "Card Type",
        "Card Category",
        "Issuer"
    ])

    writer.writerows(data)


print("CSV file created successfully")


# Insert CSV data into MySQL
with open("bin_data.csv", "r", encoding="utf-8") as file:

    reader = csv.reader(file)

    next(reader)   # Skip header

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
        row[0],
        row[1],
        row[2],
        row[3],
        row[4],
        row[0]
    )
)


# Save changes
connection.commit()

print("Data inserted into MySQL successfully")


# Close connection
cursor.close()
connection.close()

print("MySQL connection closed")