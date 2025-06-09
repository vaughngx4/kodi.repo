import os
import hashlib
import re
import zipfile
import shutil
import xml.etree.ElementTree as ET

ADDONS_DIR = './zips'
OUTPUT_XML = 'addons.xml'
OUTPUT_MD5 = 'addons.xml.md5'

# --- CONFIGURATION ---
addon_dir = "./zips"
seerr_source_dir = "../KodiSeerr"
seerr_target_dir = "./zips/plugin.video.kodiseerr"
seerr_addon_id = "plugin.video.kodiseerr"
seerr_files = ["plugin.video.kodiseerr.zip", "addon.xml", "fanart.jpg", "icon.png"]

# --- STEP 1: BUILD addons.xml and addons.xml.md5 ---
def get_addon_xml(addon_path):
    return open(os.path.join(addon_path, 'addon.xml'), encoding='utf-8').read()

def write_addons_xml():
    addons = []
    for addon in os.listdir(ADDONS_DIR):
        addon_path = os.path.join(ADDONS_DIR, addon)
        if os.path.isdir(addon_path):
            for f in os.listdir(addon_path):
                if f.endswith('.zip'):
                    continue
            xml = get_addon_xml(addon_path)
            addons.append(xml.strip())

    full_xml = "\n".join(addons) + "\n"

    with open(OUTPUT_XML, 'w', encoding='utf-8') as f:
        f.write(full_xml)

    md5 = hashlib.md5(full_xml.encode('utf-8')).hexdigest()
    with open(OUTPUT_MD5, 'w') as f:
        f.write(md5)

# --- STEP 2: ZIP repository ---
repo_id = "repository.vaughngx4"
version = "1.0.0"
source_dir = f"./{repo_id}"
output_zip_name = f"{repo_id}-{version}.zip"
output_zip_path = f"./{output_zip_name}"
destination_path = os.path.join(source_dir, output_zip_name)

def zip_repo(source_dir, output_zip_path, destination_path):
    if os.path.exists(destination_path):
        os.remove(destination_path)
        print(f"Deleted old ZIP inside folder: {destination_path}")

    if os.path.exists(output_zip_path):
        os.remove(output_zip_path)
        print(f"Deleted old ZIP in root: {output_zip_path}")

    with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, os.path.dirname(source_dir))
                zipf.write(abs_path, rel_path)
    print(f"Created new ZIP: {output_zip_path}")

    shutil.move(output_zip_path, destination_path)
    print(f"Moved ZIP into folder: {destination_path}")

zip_repo(source_dir, output_zip_path, destination_path)

# --- STEP 3: Copy KodiSeerr files and rename zip ---
# Ensure target directory exists
os.makedirs(seerr_target_dir, exist_ok=True)

# Get version from addon.xml
addon_xml_path = os.path.join(seerr_source_dir, "addon.xml")
tree = ET.parse(addon_xml_path)
root = tree.getroot()
version = root.attrib.get("version")

if not version:
    raise ValueError("Could not find version attribute in addon.xml")

# Copy and rename ZIP
source_zip = os.path.join(seerr_source_dir, f"{seerr_addon_id}.zip")
target_zip_name = f"{seerr_addon_id}-{version}.zip"
target_zip_path = os.path.join(seerr_target_dir, target_zip_name)

shutil.copy2(source_zip, target_zip_path)
print(f"Copied and renamed zip: {target_zip_path}")

# Copy remaining files
for file_name in ["addon.xml", "fanart.jpg", "icon.png"]:
    src = os.path.join(seerr_source_dir, file_name)
    dst = os.path.join(seerr_target_dir, file_name)
    shutil.copy2(src, dst)
    print(f"Copied {file_name} to {dst}")

if __name__ == "__main__":
    write_addons_xml()