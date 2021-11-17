from PIL import Image
import re
import os
import json


# Helper Functions


def format_coordinates(degrees, minutes, seconds, direction):
    value = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60)
    if direction == 'W' or direction == 'S':
        value *= -1
    return value


def save_result(filename, latitude=None, longitude=None):
    result = {
        "filename": filename,
        "latitude": latitude,
        "longitude": longitude
    }
    results.append(result)


# End Helper


image_dir = "Images"
srt_dir = "SubRip"
output_dir = "Locations"
gps_tag_key = 34853


file_type = input("File Type Extensions (e.g. jpg)... \nType:")
results = []


# Jpg Files
if file_type.upper() == "JPG":
    files = os.listdir(image_dir)
    img_files = [f for f in files if not re.search("^\\.", f)]

    for file in img_files:
        image = Image.open("{}/{}".format(image_dir, file))
        exifData = image.getexif()
        gps_data = exifData.get(gps_tag_key)

        if gps_data is not None:
            lat = gps_data[2] + (gps_data[1],)
            long = gps_data[4] + (gps_data[3],)
            save_result(file, format_coordinates(*lat), format_coordinates(*long))

        else:
            save_result(file)

# Other Files


# Save Results
file_path = "{}/{}".format(output_dir, "results.JSON")
with open(file_path, "w+") as fp:
    json.dump(results, fp, indent=1)
