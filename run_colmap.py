import os
import pycolmap
from pathlib import Path

# Define paths
BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / "subset_frames"
DATABASE_PATH = BASE_DIR / "database.db"
OUTPUT_MODEL_DIR = BASE_DIR / "sparse_model"

def run_reconstruction(image_dir, database_path, output_model_dir):
    # Ensure output directory exists
    os.makedirs(output_model_dir, exist_ok=True)

    # Step 1: Extract features into database.db
    print("[INFO] Step 1: Extracting features...")
    pycolmap.extract_features(database_path, image_dir)

    # Step 2: Sequential feature matching with optimized overlap
    print("[INFO] Step 2: Running Sequential Feature Matching (Overlap = 10)...")
    pycolmap.match_sequential(
        database_path,
        pairing_options={"overlap": 10}
    )

    # Step 3: Sparse 3D Reconstruction (Mapping)
    print("[INFO] Step 3: Running Sparse 3D Reconstruction (Mapping)...")
    maps = pycolmap.incremental_mapping(database_path, image_dir, output_model_dir)

    if len(maps) > 0:
        print(f"[SUCCESS] Reconstruction complete! Model saved to: {output_model_dir}")
        maps[0].write(output_model_dir)
    else:
        print("[ERROR] Reconstruction failed to find a continuous model.")

if __name__ == "__main__":
    run_reconstruction(IMAGE_DIR, DATABASE_PATH, OUTPUT_MODEL_DIR)