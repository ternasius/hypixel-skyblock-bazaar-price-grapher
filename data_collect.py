import requests
import sqlite3
import time

conn = sqlite3.connect("bz_data.db")
cur = conn.cursor()

# get data of initial bazaar items
bz_data = requests.get("https://api.hypixel.net/skyblock/bazaar").json()
all_products = bz_data["products"]

# turn list into "numbered" dict (1-313)
product_list = []

for product in all_products:
    product_list.append(product)

product_dict = {}
for i in range(len(product_list)):
    product_dict[i + 1] = product_list[i]
    product_dict["a" + str(i + 1)] = product_dict.pop(i + 1)  # putting "a" in front of every key so that it doesn't upset SQLite

print(product_dict)

# create a table for every product
for key, product in product_dict.items():
    cur.execute(f"CREATE TABLE IF NOT EXISTS {key} (timeUnix TEXT, buyPrice REAL, sellPrice REAL)")

req_count = 0

while True:
    bz_data = requests.get("https://api.hypixel.net/skyblock/bazaar").json()
    all_products = bz_data["products"]
    count = 0

    for key, product in product_dict.items():

        # lastUpdated is time (in milliseconds) since Jan 1, 1970
        cur.execute(f"INSERT INTO {key} (timeUnix, buyPrice, sellPrice) VALUES ({str(bz_data['lastUpdated'])},"
                    f"{float(all_products[list(product_dict.values())[count]]['quick_status']['buyPrice'])},"
                    f"{float(all_products[list(product_dict.values())[count]]['quick_status']['sellPrice'])})")
        count += 1

    req_count += 1

    conn.commit()

    print(f"Times requested this session: {req_count}")

    time.sleep(300)

conn.close()
