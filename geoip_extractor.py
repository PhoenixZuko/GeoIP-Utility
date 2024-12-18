import os
import pandas as pd
import geoip2.database
import random

# File paths
csv_file_path = 'DATA_BASE_DONT_DELETED/geolite2-country-ipv4.csv'
country_db_path = 'DATA_BASE_DONT_DELETED/GeoLite2-Country.mmdb'
asn_db_path = 'DATA_BASE_DONT_DELETED/GeoLite2-ASN.mmdb'
output_file_path_template = 'output_ip_ranges_{}.txt'
asn_filters_folder = 'ASN-FILTERS'
result_folder = 'results'
result_file_path_template = os.path.join(result_folder, 'Result_{}_{}.txt')
rest_result_file_path_template = os.path.join(result_folder, 'Rest_{}_{}.txt')

# Load data from CSV into a DataFrame
df = pd.read_csv(csv_file_path, names=['ip_start', 'ip_end', 'country'], header=None)
df['country'] = df['country'].astype(str).fillna('')

# Define functions

# Get the list of countries from the database
def list_countries(dataframe):
    return sorted(dataframe['country'].unique())

# Get the list of filter files
def list_filter_files(folder_path):
    return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# Check the country of an IP using the MMDB database
def get_country(ip, reader):
    try:
        response = reader.country(ip)
        return response.country.iso_code
    except geoip2.errors.AddressNotFoundError:
        return None

# Generate and verify IP ranges for all countries
def generate_and_verify_ip_ranges_for_all_countries(dataframe, reader):
    verified_ranges = []
    for index, row in dataframe.iterrows():
        start_ip = row['ip_start']
        end_ip = row['ip_end']
        start_country = get_country(start_ip, reader)
        end_country = get_country(end_ip, reader)
        if start_country and end_country:
            verified_ranges.append(f"{start_ip}-{end_ip}")
            print(f"Valid range: {start_ip}-{end_ip}")
        else:
            print(f"Invalid range: {start_ip}-{end_ip}")
    return verified_ranges

# Save IP ranges to a file
def save_ip_ranges_to_file(ranges, file_path):
    with open(file_path, 'w') as f:
        for ip_range in ranges:
            f.write(f"{ip_range}\n")

# Check the ASN of an IP and retrieve ASN name
def get_asn_info(ip, reader):
    try:
        response = reader.asn(ip)
        asn_number = response.autonomous_system_number
        asn_name = response.autonomous_system_organization
        return asn_number, asn_name
    except geoip2.errors.AddressNotFoundError:
        return None, None

# Read ASN list from a filter file
def read_asn_list_from_file(file_path):
    with open(file_path, 'r') as f:
        return [int(line.strip()) for line in f if line.strip().isdigit()]

# Filter IP ranges by ASN list and save results
def filter_ip_ranges_by_asn_list(file_path, asn_list, reader, included_file_path, excluded_file_path):
    included_count = 0
    excluded_count = 0
    with open(file_path, 'r') as f, open(included_file_path, 'w') as included_f, open(excluded_file_path, 'w') as excluded_f:
        for line in f:
            start_ip = line.split('-')[0]
            asn_number, _ = get_asn_info(start_ip, reader)
            if asn_number in asn_list:
                included_f.write(line)
                included_count += 1
            else:
                excluded_f.write(line)
                excluded_count += 1
        print(f"Number of included IPs: {included_count}")
        print(f"Number of excluded IPs: {excluded_count}")

# Concatenate and shuffle all result files
def concatenate_and_shuffle_results(result_folder, output_file):
    all_lines = []
    
    # Iterate through all files in the results folder
    for root, _, files in os.walk(result_folder):
        for file in files:
            file_path = os.path.join(root, file)
            # Read lines from each file and append to a list
            with open(file_path, 'r') as f:
                all_lines.extend(f.readlines())
    
    # Shuffle lines
    random.shuffle(all_lines)
    
    # Save the concatenated file
    with open(output_file, 'w') as f:
        f.writelines(all_lines)
    
    print(f"The concatenated and shuffled file was saved to {output_file}")

# Create the "results" folder if it doesn't exist
def create_results_folder():
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

# Generate IP ranges for selected countries
def generate_and_verify_ip_ranges(dataframe, country_codes, reader):
    verified_ranges = []
    for index, row in dataframe.iterrows():
        if row['country'] in country_codes:
            start_ip = row['ip_start']
            end_ip = row['ip_end']
            start_country = get_country(start_ip, reader)
            end_country = get_country(end_ip, reader)
            if start_country and end_country:
                verified_ranges.append(f"{start_ip}-{end_ip}")
                print(f"Valid range: {start_ip}-{end_ip}")
            else:
                print(f"Invalid range: {start_ip}-{end_ip}")
    return verified_ranges

# Interactive user interface
def main():
    countries = list_countries(df)
    if not countries:
        print("No countries found.")
        return

    print("Available countries:")
    for i, country in enumerate(countries, 1):
        if i % 23 == 0:
            print(country)
        else:
            print(country, end=', ')
    print()

    selected_countries = input("Enter the desired country code (0 for all, or a comma-separated list): ").strip().upper()

    if selected_countries == '0':
        country_codes = ['all_countries']
        output_file_path = 'all_countries_file.txt'
    else:
        country_codes = [code.strip() for code in selected_countries.split(',') if code.strip() in countries]
        output_file_path = output_file_path_template.format("_".join(country_codes))

    country_reader = geoip2.database.Reader(country_db_path)

    if selected_countries == '0':
        verified_ip_ranges = generate_and_verify_ip_ranges_for_all_countries(df, country_reader)
    else:
        verified_ip_ranges = generate_and_verify_ip_ranges(df, country_codes, country_reader)

    save_ip_ranges_to_file(verified_ip_ranges, output_file_path)
    print(f"\nVerified IP ranges saved to {output_file_path}")

    filter_files = list_filter_files(asn_filters_folder)
    if not filter_files:
        print(f"No filter files found in folder {asn_filters_folder}.")
        return

    print("\nAvailable filter files:")
    for i, filter_file in enumerate(filter_files, 1):
        if i % 8 == 0:
            print(f"{i}. {filter_file}")
        else:
            print(f"{i}. {filter_file}", end=', ')
    print()

    filter_choices = input("\nEnter the numbers of the desired filter files (comma-separated): ").strip()
    selected_filter_files = [filter_files[int(choice) - 1] for choice in filter_choices.split(',') if choice.isdigit() and int(choice) > 0 and int(choice) <= len(filter_files)]

    if not selected_filter_files:
        print("Invalid selection.")
        return

    asn_list = []
    for selected_filter_file in selected_filter_files:
        filter_file_path = os.path.join(asn_filters_folder, selected_filter_file)
        asn_list.extend(read_asn_list_from_file(filter_file_path))

    asn_reader = geoip2.database.Reader(asn_db_path)

    create_results_folder()

    result_file_path = result_file_path_template.format("_".join(country_codes), "_".join([f.split('.')[0] for f in selected_filter_files]))
    rest_result_file_path = rest_result_file_path_template.format("_".join(country_codes), "_".join([f.split('.')[0] for f in selected_filter_files]))

    filter_ip_ranges_by_asn_list(output_file_path, asn_list, asn_reader, result_file_path, rest_result_file_path)
    print(f"\nFiltered IP ranges saved to {result_file_path}")
    print(f"Excluded IP ranges saved to {rest_result_file_path}")

    concatenate_and_shuffle_results(result_folder, os.path.join(result_folder, 'concatenate_shuf.txt'))

if __name__ == "__main__":
    main()

