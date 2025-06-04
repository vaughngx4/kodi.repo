import os
import hashlib
import re
import zipfile
import shutil

addon_dirs = ["./zips", "./repository.vaughngx4"]
addons = []

for addons_path in addon_dirs:
    for root, dirs, files in os.walk(addons_path):
        for f in files:
            if f == "addon.xml":
                full_path = os.path.join(root, f)
                with open(full_path, "r", encoding="utf-8") as file:
                    xml_data = file.read().strip()
                    xml_data = re.sub(r'<\?xml[^>]+\?>', '', xml_data).strip()
                    addons.append(xml_data)

# Build final addons.xml
addons_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<addons>\n' + "\n".join(addons) + '\n</addons>'

with open("addons.xml", "w", encoding="utf-8-sig") as f:
    f.write(addons_xml)

md5 = hashlib.md5(addons_xml.encode("utf-8")).hexdigest()
with open("addons.xml.md5", "w") as f:
    f.write(md5)

# Package repository zip

# Configuration
repo_id = "repository.vaughngx4"
version = "1.0.0"
source_dir = f"./{repo_id}"
output_zip_name = f"{repo_id}-{version}.zip"
output_zip_path = f"./{output_zip_name}"
destination_path = os.path.join(source_dir, output_zip_name)

def zip_repo(source_dir, output_zip_path, destination_path):
    # Delete old ZIP from inside the repo folder if it exists
    if os.path.exists(destination_path):
        os.remove(destination_path)
        print(f"Deleted old ZIP inside folder: {destination_path}")

    # Delete old output ZIP if it exists in root
    if os.path.exists(output_zip_path):
        os.remove(output_zip_path)
        print(f"Deleted old ZIP in root: {output_zip_path}")

    # Create new ZIP
    with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, os.path.dirname(source_dir))
                zipf.write(abs_path, rel_path)
    print(f"Created new ZIP: {output_zip_path}")

    # Move new ZIP into the repository folder
    shutil.move(output_zip_path, destination_path)
    print(f"Moved ZIP into folder: {destination_path}")

zip_repo(source_dir, output_zip_path, destination_path)
