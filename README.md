
📍 Namma Space: Local 3D Indoor Reconstruction & Web Viewer
Namma Space is a local-first spatial computing pipeline that converts a standard smartphone indoor video into an interactive 3D point cloud model rendered directly inside a web browser. It is optimized for local CPU execution without relying on external cloud APIs or expensive LiDAR hardware.

📸 Overview & Key Features
Zero-Cloud Dependency: Complete local execution from frame extraction to 3D mapping.
CPU-Optimized SfM: Fine-tuned pycolmap parameters using sequential matching with an increased overlap window (overlap=10) to maintain continuous camera tracking through tight turns.
Browser-Based 3D Canvas: Lightweight WebGL rendering engine using Three.js and PLYLoader for zero-install, interactive 3D exploration.
Low Hardware Footprint: Designed to run on standard PC/laptop CPUs within strict execution windows.

🏗️ Technical Architecture & Pipeline

 Smartphone Indoor Video 
             │
             ▼  [Step 1: Frame Extraction]
     OpenCV (Python) ------   Extracts frames at consistent spatial intervals
             │
             ▼  [Step 2: Feature Spotting & Matching]
                              Extracts SIFT keypoints & runs sequential
        pycolmap ------       matching across adjacent frames (overlap=10)
             │
             ▼  [Step 3: Sparse 3D Reconstruction]
                              Structure-from-Motion (SfM) calculates 3D
  incremental_mapping ------  point coordinates and camera trajectories
             │
             ▼  [Step 4: Output Model]
 
    sparse_model/*.ply ------  Generates 3D spatial point cloud file
             │
             ▼  [Step 5: Interactive Web Viewer
    Three.js + WebGL ------  Renders PLY point cloud into interactive canvas
📁 Repository Structure
3D indoor/
├── extract_frames.py     # Extracts image frames from raw video via OpenCV
├── run_colmap.py         # Executes feature extraction, sequential matching, and SfM
├── index.html            # Three.js WebGL interactive 3D frontend viewer
├── downsample.py         # Utility script for frame subset downsampling
├── database.db           # SQLite database storing extracted features and matches
└── sparse_model/         # Output directory containing generated 3D model (.ply)

🚀 Getting Started
1. Prerequisites
Ensure Python 3.10+ is installed on your system. Install the required dependencies:
pip install opencv-python pycolmap pathlib

2. Video Frame Extraction
Place your walkthrough video in the project directory and run:
python extract_frames.py

3. Run Sparse 3D Reconstruction
Execute the main pipeline to generate the keypoint database and sparse 3D point cloud:
python run_colmap.py
This script executes Feature Extraction, Sequential Matching (overlap=10), and Incremental Mapping sequentially.

4. Launch the WebGL 3D Viewer
To bypass browser CORS restrictions when loading local .ply models, start a simple HTTP server:
python -m http.server 8000

Open your browser and navigate to:
http://localhost:8000

⚡ Performance Tuning & Troubleshooting
Missing Database Error (database.db does not exist):
Root Cause: Feature extraction step skipped or aborted before execution.
Resolution: Ensure pycolmap.extract_features() executes prior to feature matching in run_colmap.py.

Fragmented or Split 3D Model:
Root Cause: Insufficient overlap during camera turns or rapid movement.
Resolution: Increase sequential overlap window (pairing_options={"overlap": 10}).

Browser CORS Error:
Root Cause: Opening index.html directly via file:// protocol.
Resolution: Serve project files through a local server using python -m http.server 8000.
