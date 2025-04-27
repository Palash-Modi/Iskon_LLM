import os
import gdown

# Make sure the directory exists
os.makedirs("embeddings", exist_ok=True)
output_path = "embeddings/embeddings.pt"



drive_url = "https://drive.google.com/uc?id=17mi94fCQDxo4ENcqOQ25TN1O3lCE-W25"


gdown.download(drive_url, output_path, quiet=False)
