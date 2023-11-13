import subprocess
import sys

print("Checking for dependencies...")

# Install Dependencies
def check_and_install_dependencies():
    dependencies = ['requests']  # Add other dependencies as needed

    for dependency in dependencies:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', dependency],
                              stdout=subprocess.DEVNULL)

check_and_install_dependencies()

print("All dependencies installed.")

print("Starting the program...")

import os
import json
import csv
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import requests

def main():
    # Change the working directory to the directory of the script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    CURRENT_VERSION = "0.2"  # Update this when making changes to the script
    GITHUB_REPO_URL = "https://raw.githubusercontent.com/BRKNWAVE/MTGJSON-to-CSV/main/Commander%20Converter/commander_converter.py"
    TCGPLAYER_SKUS_API = "https://mtgjson.com/api/v5/TcgplayerSkus.json"

    def check_for_github_update():
        try:
            response = requests.get(GITHUB_REPO_URL)
            remote_script = response.text
            remote_version = remote_script.split("CURRENT_VERSION = ")[1].split("\n")[0].strip('"\'')

            if remote_version > CURRENT_VERSION:
                return True, remote_script
            else:
                return False, None
        except Exception as e:
            return False, None

    def update_script(remote_script):
        with open(__file__, 'w') as local_script:
            local_script.write(remote_script)
        print("Script updated successfully. Please restart the program.")

    def check_for_tcgplayer_update():
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(TCGPLAYER_SKUS_API, headers=headers)
            remote_data = response.json()
            remote_version = remote_data['meta']['version']

            with open('TcgplayerSkus.json', 'r', encoding='utf-8') as local_file:
                local_data = json.load(local_file)
                local_version = local_data['meta']['version']

                if remote_version > local_version:
                    return True, remote_version
                else:
                    return False, None
        except requests.exceptions.RequestException as e:
            print(f"Error updating TCGPlayer SKUs data: {e}")
            return False, None
        except Exception as e:
            print(f"Error: {e}")
            return False, None

    def update_tcgplayer_skus():
        try:
            response = requests.get(TCGPLAYER_SKUS_API)
            remote_data = response.json()
            with open('TcgplayerSkus.json', 'w', encoding='utf-8') as local_file:
                json.dump(remote_data, local_file, indent=2)
            print("TCGPlayer SKUs data updated successfully.")
        except Exception as e:
            print(f"Error updating TCGPlayer SKUs data: {e}")

    # Check for updates
    github_update_available, remote_script = check_for_github_update()
    tcgplayer_update_available, remote_version = check_for_tcgplayer_update()

    if github_update_available:
        update_choice = input("A new version of the script is available. Do you want to update? (y/n): ").lower()

        if update_choice == 'y':
            update_script(remote_script)
            return  # Exit after updating the script
        else:
            print("Skipping script update.")

    if tcgplayer_update_available:
        update_choice = input(f"New TCGPlayer SKUs data (version {remote_version}) is available. Do you want to update? (y/n): ").lower()

        if update_choice == 'y':
            update_tcgplayer_skus()
        else:
            print("Skipping TCGPlayer SKUs data update.")

    print("----------------")
    print("Commander Converter - version 0.2")
    print("----------------")

    while True:
        print_menu()
        choice = get_user_choice()

        if choice == 0:
            print("Exiting the program.")
            break
        elif choice == 1:
            # Convert a decklist
            convert_decklist()
        elif choice == 2:
            # Update TCGPlayer SKUs data
            update_tcgplayer_skus()
        else:
            print("Invalid choice. Please try again.")

def print_menu():
    print("1. Convert a decklist")
    print("2. Update TCGPlayer SKUs data")
    print("0. Exit")

def get_user_choice():
    while True:
        try:
            choice = int(input("Enter your choice: "))
            return choice
        except ValueError:
            print("Invalid input. Please enter a number.")

def convert_decklist():
    output_folder = './csv-outputs/'
    
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Prompt the user for the output filename
    output_filename = prompt_user_for_output_filename()
    output_file_path = f'{output_folder}{output_filename}.csv'

    # Read the TCGPlayer Skus JSON data
    tcgplayer_skus_path = os.path.join(os.getcwd(), 'TcgplayerSkus.json')
    with open(tcgplayer_skus_path, 'r', encoding='utf-8') as tcgplayer_skus_file:
        tcgplayer_skus_data = json.load(tcgplayer_skus_file)

    # List available decklists and prompt user for choice
    decklist_files = list_decklists()
    choice = prompt_user_for_decklist()

    if choice == 0:
        print("Exiting the program.")
    else:
        # Use the selected decklist file
        selected_decklist = decklist_files[choice - 1]
        decklist_path = f'./decklists/{selected_decklist}'

        # Read the JSON data from the selected decklist file
        with open(decklist_path, 'r', encoding='utf-8') as json_file:
            decklist_data = json.load(json_file)

        # Check for mismatches between decklist card IDs and TCGPlayer SKU IDs
        decklist_card_ids = {row.get('uuid') for section in ['commander', 'mainBoard'] for row in decklist_data['data'][section]}
        for card_id in decklist_card_ids:
            if card_id not in tcgplayer_skus_data['data']:
                print(f"Card ID {card_id} not found in TCGPlayer SKUs data.")
            else:
                skus_for_card = tcgplayer_skus_data['data'][card_id]
                if not skus_for_card:
                    print(f"No SKUs found for card ID {card_id}.")


        # Open a new CSV file and write the header row
        with open(output_file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["TCGplayer Id", "Product Line", "Set Name", "Product Name", "Title Number", "Rarity", "Condition", "TCG Market Price", "TCG Direct Low", "TCG Low Price With Shipping", "TCG Low Price", "Total Quantity", "Add to Quantity", "TCG Marketplace Price", "Photo URL"])

            # Create a set to check for duplicate TCGPlayer Ids
            seen_ids = set()

            # Write each data row to the CSV file
            for section in ['commander', 'mainBoard']:
                for row in decklist_data['data'][section]:
                    tcgplayer_sku = row.get('uuid')
                    # Fetch the TCGPlayer Sku information only for cards in the decklist
                    tcgplayer_sku_info = tcgplayer_skus_data['data'].get(tcgplayer_sku, [])

                    # Filter only Near Mint Skus for the card in the decklist
                    near_mint_skus = [sku_info for sku_info in tcgplayer_sku_info if sku_info.get('condition', '').upper() == 'NEAR MINT']

                    # If there are Near Mint Skus for the card, use the first one
                    if near_mint_skus:
                        sku_info = near_mint_skus[0]
                        condition = sku_info.get('condition', 'Near Mint')
                        language = sku_info.get('language', 'ENGLISH')
                        printing = sku_info.get('printing', 'FOIL')
                        productId = sku_info.get('productId', '')
                        skuId = sku_info.get('skuId', '')

                        # Check for duplicate TCGPlayer Ids
                        if skuId in seen_ids:
                            continue
                        seen_ids.add(skuId)

                        productName = row.get('name')
                        count = row.get('count')
                        rarity = row.get('rarity', '')[0].upper() if row.get('rarity') else ''
                        number = row.get('number')
                        productLine = 'Magic'
                        marketplacePrice = '1'

                        # Use skuId as the TCGPlayer Id in the CSV row
                        writer.writerow([skuId, '', '', productName, '', rarity, condition, '', '', '', '', '', count, marketplacePrice, ''])

        print(f"CSV file '{output_filename}.csv' has been created in the './csv-outputs/' folder.")


def list_decklists():
    decklist_folder = './decklists/'
    decklist_files = os.listdir(decklist_folder)

    print("Available Decklists:")
    for i, file in enumerate(decklist_files, start=1):
        print(f"{i}. {file}")

    print("0. Exit")
    return decklist_files

def prompt_user_for_decklist():
    while True:
        try:
            choice = int(input("Enter the number corresponding to the decklist you want to use (or 0 to exit): "))
            return choice
        except ValueError:
            print("Invalid input. Please enter a number.")

def prompt_user_for_output_filename():
    return input("Enter the desired name for the output CSV file (without extension): ")

if __name__ == "__main__":
    main()
