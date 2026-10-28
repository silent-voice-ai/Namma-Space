import os
import cv2
import imageio_ffmpeg as ffmpeg_wrapper

def extract_frames_pure_python(video_path, output_dir, fps=3, blur_threshold=100.0):
    os.makedirs(output_dir, exist_ok=True)
    
    # Get the ffmpeg binary path automatically managed by Python
    exe_path = ffmpeg_wrapper.get_ffmpeg_exe()
    print(f"[INFO] Using Python-managed FFmpeg at: {exe_path}")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    original_fps = cap.get(cv2.CAP_PROP_FPS)
    skip_interval = max(1, int(original_fps // fps))
    
    print(f"[INFO] Processing video: {video_path}")
    print(f"[INFO] Original FPS: {original_fps}, Target Extraction FPS: {fps}")

    frame_idx = 0
    saved_count = 0
    blurry_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Extract frames based on target fps interval
        if frame_idx % skip_interval == 0:
            # Convert to grayscale for Laplacian blur check
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Compute variance of Laplacian (lower score = blurrier image)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

            if laplacian_var < blur_threshold:
                blurry_count += 1
            else:
                # Save clean frame
                filename = os.path.join(output_dir, f"frame_{saved_count:05d}.jpg")
                cv2.imwrite(filename, frame)
                saved_count += 1

        frame_idx += 1

    cap.release()
    print(f"[SUCCESS] Done! Saved {saved_count} clean frames, discarded {blurry_count} blurry frames.")

if __name__ == "__main__":
    VIDEO_FILE = "tour.mp4.f616.mp4"
    OUTPUT_FOLDER = "extracted_frames"
    
    extract_frames_pure_python(VIDEO_FILE, OUTPUT_FOLDER, fps=3, blur_threshold=100.0)