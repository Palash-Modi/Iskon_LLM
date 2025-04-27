import gdown
import os

# Make sure target folder exists
os.makedirs("embeddings", exist_ok=True)


# Google Drive file URL
drive_url = "https://drive.google.com/uc?id=17mi94fCQDxo4ENcqOQ25TN1O3lCE-W25"

# Output path
output_path = "/mnt/embeddings/embeddings.pt"

# Download the file
if not os.path.exists(output_path):
    print("Downloading embeddings.pt from Google Drive...")
    gdown.download(drive_url, output_path, quiet=False)
    print("Download complete!")
else:
    print("embeddings.pt already exists, skipping download.")
