import pandas as pd
import requests
import os
from concurrent.futures import ThreadPoolExecutor
import time
from urllib.parse import urlparse
import re

# Function to sanitize filenames
def sanitize_filename(name):
    # Remove invalid characters for filenames
    return re.sub(r'[\\/*?:"<>|]', "", name)

# Function to download a single image
def download_image(row):
    try:
        image_url = row['image_url']
        bottle_id = row['id']
        bottle_name = sanitize_filename(row['name'])
        
        # Create a filename with ID and name
        filename = f"{bottle_id}.jpg"
        filepath = os.path.join(output_dir, filename)
        
        # Skip if file already exists
        if os.path.exists(filepath):
            print(f"Skipping {filename} - already exists")
            return True
        
        # Check if URL is valid
        if not image_url or pd.isna(image_url) or not str(image_url).startswith('http'):
            print(f"Skipping {bottle_id}: Invalid URL - {image_url}")
            return False
        
        # Download image with timeout
        response = requests.get(image_url, timeout=10)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")
            return True
        else:
            print(f"Failed to download {bottle_id}: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading {row.get('id', 'unknown')}: {str(e)}")
        return False

# Main execution
if __name__ == "__main__":
    # output directory
    output_dir = os.path.join(os.path.dirname(__file__), '../data/bottle_images')
    os.makedirs(output_dir, exist_ok=True)
    

    data_path = os.path.join(os.path.dirname(__file__), '../data/metadata.csv')
    

    try:
        df = pd.read_csv(data_path)
        print(f"Loaded {len(df)} bottles from CSV")
    except Exception as e:
        print(f"Error loading CSV: {str(e)}")
        print("Please make sure the CSV file exists and is properly formatted")
        exit(1)
    
    if 'image_url' not in df.columns:
        print("Error: 'image_url' column not found in the data")
        print(f"Available columns: {df.columns.tolist()}")
        exit(1)
    
    # Download images in parallel for efficiency
    print(f"Starting download of {len(df)} images...")
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(download_image, df.to_dict('records')))
    
    # Report results
    success_count = results.count(True)
    print(f"Download complete! Successfully downloaded {success_count} of {len(df)} images")