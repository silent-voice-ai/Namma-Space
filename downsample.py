import os
import shutil

# Path to your extracted frames folder
source_dir = "extracted_frames" 
target_dir = "subset_frames"

# Create target directory if it doesn't exist
os.makedirs(target_dir, exist_ok=True)

# Get all frame files
frames = sorted([f for f in os.listdir(source_dir) if f.endswith(('.jpg', '.png'))])

# Keep every 10th frame
step = 4
selected_frames = frames[::step]

print(f"Total frames originally: {len(frames)}")
print(f"Frames selected for COLMAP: {len(selected_frames)}")

# Copy selected frames to the new folder
for frame in selected_frames:
    src_path = os.path.join(source_dir, frame)
    dst_path = os.path.join(target_dir, frame)
    shutil.copy(src_path, dst_path)

print("Done! Now point your COLMAP script to the 'subset_frames' folder.")