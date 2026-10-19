import os
import urllib.request
import zipfile
import shutil

tools_dir = r"C:\Users\YOCKET-271\tools"
os.makedirs(tools_dir, exist_ok=True)

jdk_zip = os.path.join(tools_dir, "jdk17.zip")
mvn_zip = os.path.join(tools_dir, "maven.zip")

jdk_url = "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.12%2B7/OpenJDK17U-jdk_x64_windows_hotspot_17.0.12_7.zip"
mvn_url = "https://archive.apache.org/dist/maven/maven-3/3.9.6/binaries/apache-maven-3.9.6-bin.zip"

headers = {'User-Agent': 'Mozilla/5.0'}

def download_file(url, target_path):
    print(f"Downloading {url} -> {target_path} ...")
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp, open(target_path, 'wb') as out_f:
        shutil.copyfileobj(resp, out_f)
    print(f"Downloaded {target_path} successfully (size: {os.path.getsize(target_path)} bytes)")

def extract_file(zip_path, target_dir):
    print(f"Extracting {zip_path} -> {target_dir} ...")
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(target_dir)
    print(f"Extracted {zip_path} successfully")

# 1. JDK 17
if not any(d.startswith("jdk-17") for d in os.listdir(tools_dir)):
    download_file(jdk_url, jdk_zip)
    extract_file(jdk_zip, tools_dir)
    if os.path.exists(jdk_zip):
        os.remove(jdk_zip)
else:
    print("JDK 17 folder already exists.")

# 2. Maven 3.9.6
if not any(d.startswith("apache-maven") for d in os.listdir(tools_dir)):
    download_file(mvn_url, mvn_zip)
    extract_file(mvn_url, tools_dir)
    if os.path.exists(mvn_zip):
        os.remove(mvn_zip)
else:
    print("Maven folder already exists.")

print("All tools configured successfully!")
