import os
import gdown

# Make sure the directory exists
os.makedirs("/mnt/embeddings", exist_ok=True)

drive_url = "https://drive.google.com/uc?id=17mi94fCQDxo4ENcqOQ25TN1O3lCE-W25"
output_path = "/mnt/embeddings/embeddings.pt"

gdown.download(drive_url, output_path, quiet=False)
