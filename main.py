import datetime
import sqlite3
import requests

import pandas as pd
import plotly.graph_objects as go

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

conn = sqlite3.connect("bz_data.db")
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

line_mode = "lines"

want_add_marker = True

while want_add_marker:
    response = str(input("Add markers? (Y/N): "))
    if response.upper() == "Y":
        line_mode = "lines+markers"
        want_add_marker = False
    elif response.upper() == "N":
        want_add_marker = False
    else:
        print("invalid input, try again")


fig = go.Figure()
fig.add_trace(go.Scatter(x=x_axis,
                         y=buy_y_axis,
                         mode=f"{line_mode}",
                         name="Buy Price"))
fig.add_trace(go.Scatter(x=x_axis,
                         y=sell_y_axis,
                         mode=f"{line_mode}",
                         name="Sell Price"))
fig.update_layout(title=f"{product_name}",
                  xaxis_title="Date",
                  yaxis_title="Price")
fig.update_xaxes(rangebreaks=[dict(bounds=[24, 12], pattern="hour")])  # bounds is here so points at times when i sleep don't connect

want_from_zero = True

while want_from_zero:
    response = str(input("Make the Y-axis start at zero? (Y/N): "))
    if response.upper() == "Y":
        fig.update_yaxes(rangemode="tozero")
        want_from_zero = False
    elif response.upper() == "N":
        want_from_zero = False
    else:
        print("invalid input, try again")

fig.show()
