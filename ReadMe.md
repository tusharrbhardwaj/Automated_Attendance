# Automated Attendance Marking System


## Project overview

This project automates the process of marking attendance on an educational platform (designed for `study.gisma.com` in this implementation). It uses Selenium to log in, navigate to a chosen module, extract the student roster, and then compare that roster with an attendance list (CSV exported from another source) to produce `present` and `absent` lists and archive results by date.

Main features:
- Headless Selenium-based browser automation to login and navigate modules.
- Student roster extraction (saved as a `.txt` file).
- Parsing of exported attendance CSV to extract present students and validate date.
- Comparison between roster and attendance list to produce `present` and `absent` files.
- Simple organizer to move module files into a folder named after the attendance date.
- A small `initializer` utility to create `config.json` containing login credentials.

---

## Repository structure (files & purpose)
```bash
Automated_Attendance/
├─ main.py # Orchestrator: checks config, calls automation, comparison, organizer
├─ automation.py # Selenium logic: startup(), login(), navigate_module(), data_extraction(), ...
├─ initializer.py # Creates config.json (stores id & password)
├─ information.py # Reads and validates attendance CSV; extracts date and names
├─ data_comparsion.py # (comparison + organizer) compares roster and attendance, creates present/absent files
├─ requirements.txt # Python dependencies (generated)
├─ README.md # This file
└─ config.json # (created via initializer.py) stores credentials (NOT in repo)
```
---
## Installation & setup

1. Make sure you have **Python 3.8+** installed (**Python 14.0 recommended).

2. Install required packages:

```bash
pip install -r requirements.txt
```
Or
3. Install these packages one by one

```bash
pip install pyinputplus
pip install colorama
pip install selenium
pip install beautifulsoup4
pip install requests
```

3. Install Google Chrome (or Chromium) on the machine that will run the script. The repo uses webdriver-manager which will automatically download a compatible ChromeDriver. (No need to do it manually, It is added in automation.py file and will be executed once you run main.py)

---

## Usage (typical flow)
Ensure config.json exists (run initializer if it does not) Or Directly run main.py, it contains funcationalities to redirect user to intializer.py depending on the availablity of config.json

Run the main program:
```bash
python main.py
```
High-level flow the script performs:
* Reads credentials from config.json (automation.login_data()).
* Starts Selenium and opens the site (automation.startup()).
* Logs in (automation.login(eid, pwd)) and verifies login (automation.login_verification()).
* Prompts user for a module code (e.g. CS101) and navigates to that module (automation.navigate_module()).
* Navigates to the module "People" or "Attendance" page and filters to students (automation.navigating_student()).
* Extracts the roster and writes it to <MODULE>_students_list.txt.
* Prompts user for the attendance CSV filename (without extension). The CSV will be processed by information.main() which:
** Validates CSV existence
** Extracts the attendance date from the CSV (expects a date in format YYYY-MM-DD inside the CSV raw data)
** Writes <attendance_date>.txt containing present students (derived from CSV)
** The script renames and compares files to produce <module>_attendance_list.txt, and creates <module>_present.txt and <module>_absent.txt.


### Finally, files are organized into a folder named after the attendance date.

---

# Expected input / CSV format
The information.py code expects:
* A CSV where the first non-header row contains a raw date string in a column that matches the regex \d{4}-\d{2}-\d{2}.(yyyy-mm-dd format)
* The code reads raw_date = data[0][0] — i.e., it expects the date to be found in column 0 of the first data row.
* Student names are extracted using students[-2] (so the name column is expected to be the penultimate column in each row).
* If your attendance CSV uses a different structure, you will need to adapt information.ReadFile() to the column layout used by your export.

---

# Important implementation notes & known issues

* Headless mode: 
```bash
automation.startup() 
```
runs Chrome in headless mode 
```bash 
(options.add_argument("--headless=new"))
```
* For debugging Visual/interaction issues, remove that argument or run with a visible browser.

* Hardcoded scroll value: data_extraction() uses window.scrollTo(0, window.scrollY + 10600) to load more page content; this value might need tuning for different layouts or longer pages.

* Names written without newline (in some places): some functions write student names without \n — ensure extracted names are written line-separated (the current cleaned versions included here write '\n').

* Edge cases: If Canvas changes the DOM, XPath/Selectors may break. Use robust selectors (IDs, data attributes), or add retries and better error output.

* Security: config.json stores plaintext credentials. Consider environment variables, keyring, or prompting the user each run for better security.

---

# Troubleshooting 

* selenium.common.exceptions.NoSuchElementException — Element XPATH changed; open the page in normal browser and inspect the target element; update the selectors in automation.py.

* webdriver-manager fails to download a ChromeDriver — ensure Chrome is installed and the environment has internet access.

* pyinputplus prompts not working — check terminal encoding; test in an interactive shell.

* If output files are empty or have concatenated names, verify that parsing logic (BeautifulSoup selectors and CSV column indices) match the actual site and CSV format.

---

# Future Scope 

Add a mode to mark attendance automatically (instead of only extracting roster and comparing).

---
**Author:** Tushar Bharadwaj  
**Language:** Python  
**Status:** Prototype / Work in progress