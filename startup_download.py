import os
import gdown
import hashlib

def file_checksum(path, algo="md5"):
    """Compute checksum of a file."""
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def download_embeddings():
    # Config
    os.makedirs("embeddings", exist_ok=True)
    output_path = "embeddings/embeddings.pt"
    drive_url = "https://drive.google.com/uc?id=17mi94fCQDxo4ENcqOQ25TN1O3lCE-W25"

    # Expected checksum (OPTIONAL: only if you know it)
    expected_md5 = "d41d8cd98f00b204e9800998ecf8427e"  # ← placeholder, replace with real if known

    if os.path.exists(output_path):
        print(f"✅ Found existing embeddings at '{output_path}'. Verifying checksum...")

        # Checksum verification
        actual_md5 = file_checksum(output_path)
        if expected_md5 and actual_md5 != expected_md5:
            print(f"⚠️ Checksum mismatch (expected {expected_md5}, got {actual_md5}). Re-downloading...")
            gdown.download(drive_url, output_path, quiet=False)
            print("✅ Download complete.")
        else:
            print("✅ Checksum verified. Skipping download.")
    else:
        print(f"⬇️ Downloading embeddings to '{output_path}'...")
        gdown.download(drive_url, output_path, quiet=False)
        print("✅ Download complete.")

# Allow running manually too
if __name__ == "__main__":
    download_embeddings()
