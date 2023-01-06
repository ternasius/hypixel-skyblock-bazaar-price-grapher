# hypixel-skyblock-bazaar-price-grapher
data_collect.py:
  - this will request data from Hypixel's API every 5 minutes and store it in a database
  - leave it running as long as you want

main.py:
  - you will be asked to input a key, the key will come in the form of "a(num)"
    - type in "LIST" if you want a list of all the keys
  - the program will then produce a graph of the item's sell and buy price from data collected in the database
