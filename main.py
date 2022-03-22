import datetime
import sqlite3
import requests

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

bz_data = requests.get("https://api.hypixel.net/skyblock/bazaar").json()
all_products = bz_data["products"]


# turn list into "numbered" dict (1-313)
product_list = []

for product in all_products:
    string = product
    new_str = ""

    for pos, char in enumerate(string):
        new_str += char

    product_list.append(new_str)

product_dict = {}
for i in range(len(product_list)):
    product_dict[i + 1] = product_list[i]
    product_dict["a" + str(i + 1)] = product_dict.pop(i + 1)  # putting "a" in front of every key so that it doesn't upset SQLite

# start of main function
choosing_product = True
product_id = ""
product_name = ""

# ask for product to graph, also lists all available product and its corresponding keys
while choosing_product:
    product_id = str(input("Type in a KEY to pick a product to show (type 'LIST' to display all available products): "))
    if product_id.upper() == "LIST":
        for key, product in product_dict.items():
            print(key + ": " + product)
    else:
        for key, product in product_dict.items():
            if product_id == key:
                product_name = product
                choosing_product = False

conn = sqlite3.connect(r"C:\Programming\Hypixel Skyblock Thing\bz_data.db")
cur = conn.cursor()

x_axis = []
buy_y_axis = []
sell_y_axis = []
for row in cur.execute(f"SELECT timeUnix FROM {product_id}"):
    x_axis.append(datetime.datetime.fromtimestamp((int(row[0]) / 1000), datetime.timezone(datetime.timedelta(hours=-7))))
for row in cur.execute(f"SELECT buyPrice FROM {product_id}"):
    buy_y_axis.append(float(row[0]))
for row in cur.execute(f"SELECT sellPrice FROM {product_id}"):
    sell_y_axis.append(float(row[0]))


conn.close()

df_buy = pd.DataFrame(dict(
    x=x_axis,
    y=buy_y_axis
))
df_sell = pd.DataFrame(dict(
    x=x_axis,
    y=sell_y_axis
))

fig = go.Figure()
fig.add_trace(go.Scatter(x=x_axis,
                         y=buy_y_axis,
                         mode="lines+markers",
                         name="Buy Price"))
fig.add_trace(go.Scatter(x=x_axis,
                         y=sell_y_axis,
                         mode="lines+markers",
                         name="Sell Price"))
fig.update_layout(title=f"{product_name}",
                  xaxis_title="Date",
                  yaxis_title="Price")
fig.show()
