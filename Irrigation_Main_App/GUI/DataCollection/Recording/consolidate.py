from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import csv


def ConsolidateData(image_folder: str, output_folder: str):
    path_to_images = Path(image_folder)
    post_processing_images = Path(output_folder)
    
    post_processing_images.mkdir(parents=True,exist_ok=True)
    
    moistures = []
    with open (path_to_images/"moistures.csv", newline="") as csv_file:
        reader = csv.reader(csv_file)
        try:
            header = next(reader)  # skip header
        except StopIteration:
            return False
        for row in reader:
            if row:  # skip empty lines
                moistures.append(row)

        if not moistures:  #  no actual data rows found
            return False
        
    imgs = sorted([f.name for f in path_to_images.iterdir() if f.suffix.lower() != ".csv"])

    entries = [(imgs[i],moistures[i]) for i in range(min(len(imgs), len(moistures)))]

    for i, (img_name, moisture) in enumerate(entries, start=1):
        img_path = path_to_images / img_name
        img = Image.open(img_path)
        draw = ImageDraw.Draw(img)
        moisture_value = float(moisture[0])  # extract and convert
        draw.text((10, 10), f"Moisture: {round(moisture_value)}", fill=(255, 255, 0))
        img.save(post_processing_images / f"{i}.jpg")

    return True