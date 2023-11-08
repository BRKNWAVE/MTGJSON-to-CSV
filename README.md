## Running this Python Script on a Fresh Machine

This guide will walk you through the process of running this Python script on a machine that doesn't have Python installed.

### Step 1: Install Python

1. Download the latest version of Python from the [official website](https://www.python.org/downloads/).
2. Run the installer. During the installation, make sure to check the box that says "Add Python to PATH" before you click "Install Now".

### Step 2: Verify Python Installation

1. Open a new command prompt or terminal window.
2. Type `python --version` and press Enter. You should see the Python version number that you just installed.

### Step 3: Install Necessary Python Packages

This script requires the `json` and `csv` packages. These are part of the Python Standard Library, so you don't need to install them separately.

### Step 4: Run the Script

1. Download the `commander_converter.py` script and the `decklist.json` file and put them in the same directory.
2. Open a command prompt window and navigate to the directory where you saved the script and the JSON file.
    - alternatively, right click the `commander_converter.py` script and `Run in Terminal...`
3. Type `python commander_converter.py` and press Enter. The script should run and create a new CSV file in the same directory.

If you encounter any errors:
    - Reverify the integrity of your Python installation
    - Ensure the file name for the JSON file you wish to convert is `decklist.json` 
    - Ensure the `commander_converter.py` script and the `decklist.json` file are in the same directory
    - Ensure the JSON file is sourced from MTGJSON's Decklists found [here](https://mtgjson.com/downloads/all-decks/)
    - Ensure the JSON file is of the type "Commander Deck" on MTGJSON