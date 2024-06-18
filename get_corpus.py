# Author: Hugo Keenan
# Aim: This script retrieves article data from the NYT archive API for a user specified year range and saves it to a file of each month's data before concatenating all individual files into a single CSV file.
## Note: It saves each month's data to a separate file in the /corpus directory. concat_data function concatenates files in folder to a single file.
## Note: To run this script successfully, you need to get your API key from the NYT Developer site and save it in a file called "nyt_api_key.txt"

import csv
import requests
import os
import time
import logging
import argparse
from tqdm import tqdm

# Constants
OUT_DIR = 'corpus'
API_KEY_FILE_PATH = 'nyt_api_key.txt'
BASE_URL = 'https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key={key}'
MAX_RETRY = 10
RETRY_DELAY = 1
CHR255 = chr(255)

def fetch_from_api(year, month, key, logger, retry_count=0):
    """
    Try to get data from the API. If the request fails with a 429 status code (Too many requests),
    retry after an exponentially increasing amount of time.
    Info is logged to the logger.
    """
    url = BASE_URL.format(year=year, month=month, key=key)
    logger.info('Fetching {}'.format(url))
    try:
        res = requests.get(url)
        res.raise_for_status()  # Raise an exception for any HTTP error status
        return res.json()
    except requests.HTTPError as e:
        if e.response.status_code == 429:
            if retry_count < MAX_RETRY:
                # Exponential backoff: Wait for an exponentially increasing amount of time before retrying.
                delay = (2 ** retry_count) * RETRY_DELAY
                logger.info('Got HTTP 429: Too many requests. Retrying in {} seconds.'.format(delay))
                time.sleep(delay)
                return fetch_from_api(year, month, key, logger, retry_count + 1)
            else:
                logger.error('Max retry limit reached. Unable to fetch data.')
                raise
        else:
            logger.error('HTTP Error: {}'.format(e))
            raise

# Function to read API key from file
def read_api_key_from_file(file_path, logger):
    try:
        with open(file_path, 'r') as file:
            api_key = file.read().strip()
        return api_key
    except FileNotFoundError:
        logger.error(f"API key file '{file_path}' not found.")
        raise
    except Exception as e:
        logger.error(f"Error reading API key file: {e}")
        raise

def extract_metadata(api_results):
    """
    Extract metadata from the API response
    """
    all_metadata = []
    for doc in api_results['response']['docs']:
        metadata = {
            'title': doc['headline']['main'],
            'section_name': doc['section_name'],
            'snippet': doc['snippet'],
            'lead_paragraph': doc['lead_paragraph'],
            'year': doc['pub_date'][:4],
            'month': doc['pub_date'][5:7],
            'web_url': doc['web_url']
        }
        all_metadata.append(metadata)

    return all_metadata

def save_to_csv(data, file_path, delimiter="|||||", missing_value="NA"):
    """
    Saves a list of dictionaries to a CSV file with the 
    """
    # save as CSV with delimiter = chr(255)
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys(), delimiter=CHR255)
        writer.writeheader()
        for row in data:
            # Replace missing values with "NA"
            row = {key: value if value else missing_value for key, value in row.items()}
            writer.writerow(row)
    # re open and replace delimiter with "|||||"
    with open(file_path, 'r') as file:
        text = file.read()
        text = text.replace(CHR255, delimiter)
    with open(file_path, 'w') as file:
        file.write(text)

def load_from_csv(file_path, delimiter="|||||"):
    """
    Load data from a CSV file with a custom delimiter
    """
    file_name, file_extension = os.path.splitext(file_path)
    with open(file_path, 'r') as file:
        text = file.read()
        text = text.replace(delimiter, CHR255)
    temp_file_path = f"{file_name}_temp.{file_extension}"
    with open(temp_file_path, 'w') as file:
        file.write(text)
    with open(temp_file_path, 'r', newline='') as file:
        reader = csv.DictReader(file, delimiter=CHR255)
        data = [row for row in reader]
    # remove the temp file
    os.remove(temp_file_path)
    return data



def get_corpus(start_year, end_year, logger, delimiter = '|||||', missing_value='NA'):
    if logger is None:
        logger = logging.getLogger('NYT downloader')
    # Get the API key
    try:
        NYT_KEY = read_api_key_from_file(API_KEY_FILE_PATH, logger)
    except Exception:
        logger.error("Unable to retrieve API key. Exiting.")
        exit(1)
        
    # Make sure dir exists
    os.makedirs(OUT_DIR, exist_ok=True)
    
    # Fetch data from the API
    for year in range(start_year, end_year + 1):
        for month in range(1,13):
            file_path = os.path.join(OUT_DIR, f'nyt_data_{year}_{month}.csv')
            if os.path.exists(file_path):
                logger.info(f"Data for {year}-{month} already exists. Skipping.")
                continue
            logger.info(f"Fetching data for {year}-{month}...")
            try:
                api_results = fetch_from_api(year, month, NYT_KEY, logger)
                metadata = extract_metadata(api_results)
                logger.info(f"Successfully fetched {len(metadata)} articles.")
            except Exception as e:
                logger.error(f"Error fetching data for {year}-{month}: {e}")
                continue
            save_to_csv(metadata, file_path, delimiter=delimiter, missing_value=missing_value)
            logger.info(f"Data saved to {file_path}")
    
def concat_data(out_file='all_nyt_data.csv', dir_path=OUT_DIR, logger=None):
    if logger is None:
        logger = logging.getLogger('NYT downloader')
    # Get all file paths
    file_paths = [os.path.join(dir_path, file) for file in os.listdir(dir_path) if file.endswith('.csv')]
    logger.info(f"Found {len(file_paths)} files.")
    # Load data from each file
    all_data = []
    logger.info("Loading data...")
    for file_path in tqdm(file_paths):
        data = load_from_csv(file_path)
        all_data.extend(data)
    # Save all data to a single file
    logger.info(f"Saving data to {out_file}, may take a while...")
    save_to_csv(all_data, out_file)


if __name__ == '__main__':
    # Set up logging
    logger = logging.getLogger('NYT downloader')
    logging.basicConfig(level=logging.INFO)
    
    # Get arguments from the command line
    parser = argparse.ArgumentParser(description='Download New York Times corpus for a given year and month.')
    # get the year and month (default to 2023 and 1)
    parser.add_argument('--start_year', default=1930, type=int, help='Year to download data from')
    parser.add_argument('--end_year', default=2023, type=int, help='Year to download data till')
    args = parser.parse_args()

    # Call the main function
    get_corpus(args.start_year, args.end_year, logger)
