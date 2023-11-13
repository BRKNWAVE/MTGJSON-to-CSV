# MTGJSON-to-CSV Converter

## Overview

This Python script is designed for converting Magic: The Gathering (MTG) decklists in JSON format to CSV format. It also provides functionality to update TCGPlayer SKU data used in the conversion process.

## Features

- **Dependency Installation:** The script checks and installs required dependencies, including the 'requests' library.

- **Automatic Updates:** The script checks for updates on GitHub. If a new version is available, users can choose to update the script.

- **TCGPlayer SKU Data Updates:** The script checks for updates to the TCGPlayer SKU data. If a new version is available, users can choose to update the data.

- **Conversion of Decklists:** Users can convert MTG decklists from JSON to CSV format. The script validates card IDs against TCGPlayer SKUs and identifies any mismatches.

## Getting Started

1. Ensure Python is installed on your system. If it is not you can download it from [here](https://www.python.org/downloads/).
2. Run the script by executing `python3 commander_converter.py` in your terminal or command prompt.

## Usage

1. The script prompts to update the main script if a new version is available.
2. It checks for updates to the TCGPlayer SKU data and prompts to update if a new version is available.
3. After updates, the main menu displays with options:
    - **Convert a decklist:** Convert an MTG decklist from JSON to CSV.
    - **Update TCGPlayer SKUs data:** Manually update the TCGPlayer SKU data.
    - **Exit:** Terminate the program.

## Example Decklist Conversion

1. Choose option 1 from the main menu.
2. Select the desired decklist from the available options.
3. Enter a name for the output CSV file when prompted.
4. The script converts the decklist, validating card IDs against TCGPlayer SKUs, and generates a CSV file in the 'csv-outputs' folder.

## Obtaining Decklists

To use the MTGJSON-to-CSV Converter, you need Magic: The Gathering decklists in JSON format. Follow these steps to obtain and use the decklists:

1. Visit [MTGJSON Downloads](https://mtgjson.com/downloads/all-decks/) to download the desired decklists in the uncompressed JSON format.

2. After downloading the decklists, place the JSON files in the 'decklists' folder of the MTGJSON-to-CSV Converter.

    ```
    /MTGJSON-to-CSV
    ├── commander_converter.py
    ├── csv-outputs
    ├── decklists
    │   ├── decklist1.json
    │   ├── decklist2.json
    │   └── ...
    ├── README.md
    └── ...
    ```

3. Run the script (`python3 commander_converter.py`) and use the provided options to convert the decklists to CSV or update TCGPlayer SKU data.

**Note:** Make sure to use decklists in the correct JSON format as provided by MTGJSON. The script expects valid Magic: The Gathering decklist JSON files for accurate conversion.

## Notes

- The script uses multi-threading for faster TCGPlayer SKU data updates.
- It checks for duplicate TCGPlayer IDs during decklist conversion to avoid redundancy.
- Restart the program after updating the main script.

## Disclaimer

This script is provided as-is, and the user assumes all responsibility for its use. It is not affiliated with MTGJSON or TCGPlayer.

**Author:** Ailric Bean

**Version:** 0.2

For more information if you've found this elsewhere, or to report issues, visit the [GitHub repository](https://github.com/BRKNWAVE/MTGJSON-to-CSV).
