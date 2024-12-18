# GeoIP-Range-Extractor

`GeoIP-Range-Extractor` is a powerful and customizable Python tool designed to extract IP ranges based on country or ASN (Autonomous System Number) filters. It leverages MaxMind GeoLite2 databases for accurate data processing and is ideal for use cases such as network monitoring, cybersecurity analysis, and IP range management.

---

## Features
- **Country-Based IP Extraction**: Extract IP ranges based on specific country codes.
- **ASN Filtering**: Filter IP ranges by ASN for more granular results.
- **Database Updater**: Automatically download and update GeoLite2 databases for accurate IP lookup.
- **Randomized Concatenation**: Combine and shuffle results for further analysis or custom applications.
- **Masscan Compatibility**: Generate IP ranges in a format ready to use with Masscan.
- **User-Friendly**: Fully customizable with clear folder structures for easy usage.

---

## Folder Structure
```plaintext
GeoIP-Range-Extractor/
├── geoip_extractor.py         # Main script for extracting IP ranges by country or ASN
├── update_geoip_db.py         # Script for updating GeoLite databases, saving them in the DATA_BASE_DONT_DELETED folder
├── ASN-FILTERS/               # Folder containing ASN filter files
│   ├── amazon.txt             # Example filter file for Amazon ASN numbers (one per line)
│   ├── microsoft.txt          # Example filter file for Microsoft ASN numbers
│   └── ...
├── DATA_BASE_DONT_DELETED/    # Folder where GeoLite .mmdb files are stored
│   ├── GeoLite2-Country.mmdb  # GeoLite database for country lookups
│   ├── GeoLite2-ASN.mmdb      # GeoLite database for ASN lookups
│   ├── geolite2-country-ipv4.csv # CSV file for additional country data
│   └── ...
├── results/                   # Folder for generated results
│   ├── Result_<country>_<filter>.txt     # Results filtered by ASN within the selected country
│   ├── Rest_<country>_<filter>.txt       # Remaining results for the country without filtered ASNs
│   └── concatenate_shuf.txt               # Final results (filtered + unfiltered), shuffled randomly
├── asn_list.txt               # Informal list of ASN numbers and names (used for creating filters)
├── README.md                  # Project documentation
├── LICENSE                    # Project license
└── requirements.txt           # List of required Python libraries
```

---

## Installation

### Prerequisites
1. **Python 3.7+**: Make sure Python is installed on your machine.
2. **Dependencies**: Install required libraries using the following command:
   ```bash
   pip install -r requirements.txt
   ```

### Clone the Repository
```bash
git clone https://github.com/PhoenixZuko/GeoIP-Range-Extractor.git
cd GeoIP-Range-Extractor
```

---

## Usage

### Step 1: Update GeoLite2 Databases
Run the `update_geoip_db.py` script to download and update the GeoLite2 databases:
```bash
python3 update_geoip_db.py
```

### Step 2: Extract IP Ranges
Run the main script `geoip_extractor.py`:
```bash
python3 geoip_extractor.py
```

#### Input Options
- **All Countries**: Enter `0` to extract IP ranges for all available countries.
- **Specific Countries**: Enter one or more country codes, separated by commas (e.g., `US,DE,FR`). Use the exact country codes displayed in the terminal.

#### Example Inputs
- To extract IP ranges for all countries:
  ```plaintext
  Enter country codes (0 for all countries or use comma-separated values): 0
  ```
- To extract IP ranges for the United States, Germany, and France:
  ```plaintext
  Enter country codes (0 for all countries or use comma-separated values): US,DE,FR
  ```

### Step 3: Filter Results by ASN
Use the provided ASN filter files to refine your results. Place the desired filter file (e.g., `amazon.txt`) in the `ASN-FILTERS/` folder.

---

## Output
The extracted results will be saved in the `results/` folder:
- `Result_<country>_<filter>.txt`: Filtered results by ASN.
- `Rest_<country>_<filter>.txt`: IP ranges not matching the ASN filters.
- `concatenate_shuf.txt`: Combined and randomized results.

These results are compatible with Masscan, enabling easy network scanning for specific IP ranges or ASNs.

---

## Customization

### ASN Filters
Add or modify files in the `ASN-FILTERS/` folder. Each file should contain ASN numbers (one per line) to filter the results.

### GeoLite2 Databases
Place the required `.mmdb` files in the `DATA_BASE_DONT_DELETED/` folder:
- `GeoLite2-Country.mmdb`
- `GeoLite2-ASN.mmdb`
- `geolite2-country-ipv4.csv`

---

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Author
This project was created and maintained by **PhoenixZuko**.

GitHub Profile: [Andrei Sorin](https://github.com/PhoenixZuko)

