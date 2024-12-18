import requests
import os

# Dictionary containing URLs and their corresponding local filenames
files_to_download = {
    'https://raw.githubusercontent.com/sapics/ip-location-db/main/geolite2-country/geolite2-country-ipv4.csv': 'DATA_BASE_DONT_DELETED/geolite2-country-ipv4.csv',
    'https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-ASN.mmdb': 'DATA_BASE_DONT_DELETED/GeoLite2-ASN.mmdb',
    'https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-City.mmdb': 'DATA_BASE_DONT_DELETED/GeoLite2-City.mmdb',
    'https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-Country.mmdb': 'DATA_BASE_DONT_DELETED/GeoLite2-Country.mmdb'
}

# Function to download a file
def download_file(url, dest):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(dest, 'wb') as file:
                file.write(response.content)
            print(f'Successfully updated file: {dest}')
        else:
            print(f'Error downloading file {dest}: {response.status_code}')
    except Exception as e:
        print(f'An error occurred while downloading {dest}: {e}')

# Function to update files
def update_files():
    for url, file_name in files_to_download.items():
        if os.path.exists(file_name):
            print(f'Updating file: {file_name}...')
        else:
            print(f'File {file_name} does not exist. Downloading...')
        download_file(url, file_name)

# Run the update function
if __name__ == '__main__':
    update_files()

