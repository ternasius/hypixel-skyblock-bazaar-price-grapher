# Hypixel Skyblock Bazaar Price Grapher
A tool to collect and visualize price data from the Hypixel Skyblock Bazaar.

## Components

### data_collect.py
- Collects real-time price data from the Hypixel API.
- Automatically fetches data every 5 minutes
- Stores information in a local database
- Runs continuously until manually stopped

### main.py
- Generates price graphs based on collected data.

## Usage
Run the program  
Enter an item key in the format `a(num)`  
View the generated price graph showing:  
- Buy orders
- Sell offers
- Price trends over time

## Commands
Type `LIST` to view all available item keys  
Enter a valid item key (e.g., `a1`, `a2`) to generate a graph  

## Requirements
Python 3.x
Required Python packages:
- pandas
- plotly
- sqlite3

## Setup
Clone the repository
Install dependencies
Run `data_collect.py` to begin gathering data
Use `main.py` to visualize the results

## Notes
Longer data collection periods will result in more detailed graphs
Keep `data_collect.py` running to maintain up-to-date information
