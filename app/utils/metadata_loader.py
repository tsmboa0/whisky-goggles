import csv

def load_metadata(csv_path):
    """
    Load metadata from a CSV file. Expects columns: id, name, region, abv, image_url.
    Returns a list of dictionaries for each whisky.
    """
    metadata = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse and clean fields
            try:
                wid = int(row.get("id", "").strip())
            except:
                wid = row.get("id", "").strip() or None
            name = row.get("name", "").strip()
            region = row.get("region", "").strip() or None
            # Parse ABV to float if possible
            abv_str = row.get("abv", "").replace("%", "").strip()
            avg_msrp = row.get("avg_msrp", "").strip() or None
            fair_price = row.get("fair_price", "").strip() or None
            shelf_price = row.get("shelf_price","").strip() or None
            try:
                abv = float(abv_str) if abv_str else None
            except:
                abv = None
            try:
                avg_msrp = float(avg_msrp) if avg_msrp else None
            except:
                avg_msrp = None
            try:
                fair_price = float(fair_price) if fair_price else None
            except:
                fair_price = None
            try:
                shelf_price = float(shelf_price) if shelf_price else None
            except:
                shelf_price = None

            image_url = row.get("image_url", "").strip() or None
            item = {"id": wid, "name": name, "region": region, "abv": abv, "image_url": image_url, "avg_msrp":avg_msrp, "fair_price":fair_price, "shelf_price":shelf_price}
            metadata.append(item)
    return metadata
