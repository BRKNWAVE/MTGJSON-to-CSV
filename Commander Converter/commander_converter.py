import os
import json
import csv

# Change the working directory to the directory of the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Read the JSON data from a file or API endpoint
with open('decklist.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Open a new CSV file and write the header row
with open('decklist_output.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["TCGplayer Id", "Product Line", "Set Name", "Product Name", "Title Number", "Rarity", "Condition", "TCG Market Price", "TCG Direct Low", "TCG Low Price With Shipping", "TCG Low Price", "Total Quantity", "Add to Quantity", "TCG Marketplace Price", "Photo URL"])
    
    # Write each data row to the CSV file
    for section in ['commander', 'mainBoard']:
        for row in data['data'][section]:
            tcgplayerProductId = row['identifiers'].get('tcgplayerProductId')
            productName = row.get('name')
            count = row.get('count')
            rarity = row.get('rarity', '')[0].upper() if row.get('rarity') else ''
            condition = 'Near Mint'
            number = row.get('number')
            productLine = 'Magic'
            marketplacePrice = '1'
            writer.writerow([tcgplayerProductId, '', '', '', '', '', '', '', '', '', '', '', count, marketplacePrice, ''])