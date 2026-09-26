import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://bintable.com"
SCHEMES_URL = f"{BASE_URL}/card-schemes"


# Get card schemes page
response = requests.get(SCHEMES_URL, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")


# Store scheme URLs
scheme_urls = []

for link in soup.find_all("a", href=True):

    href = link["href"]

    if href.startswith("scheme/"):

        scheme_url = urljoin(BASE_URL, href)

        if scheme_url not in scheme_urls:
            scheme_urls.append(scheme_url)


print("Total schemes:", len(scheme_urls))


# Open CSV file
with open(
    "bin_data_v2.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    # CSV header
    writer.writerow([
        "BIN/IIN",
        "Network/Scheme",
        "Card Type",
        "Card Category",
        "Issuer"
    ])


    # Process all discovered schemes
    for scheme_url in scheme_urls:

        page_url = scheme_url

        while page_url:

            print("Scraping:", page_url)

            try:
                response = requests.get(page_url, timeout=10)
                response.raise_for_status()

            except requests.RequestException as e:
                print(f"Skipping page {page_url}: {e}")
                break


            soup = BeautifulSoup(response.text, "html.parser")

            table = soup.find("table")

            if not table:
                break

            rows = table.find_all("tr")

            for row in rows[1:]:

                cells = row.find_all("td")

                if len(cells) != 5:
                    continue

                bin_iin = cells[0].get_text(strip=True)
                network = cells[1].get_text(strip=True)
                card_type = cells[2].get_text(strip=True)
                card_category = cells[3].get_text(strip=True)
                issuer = cells[4].get_text(strip=True)

                # Write one record directly to CSV
                writer.writerow([
                    bin_iin,
                    network,
                    card_type,
                    card_category,
                    issuer
                ])


            # Find next page
            next_link = soup.find("a", rel="next")

            if next_link is None:
                break

            page_url = next_link["href"]


print("Scraping completed")