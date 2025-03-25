import os
import subprocess
import argparse
import json

def download_video(video_url, output_dir):
    """Download and merge a single video with audio."""
    print(f"\n🔹 Processing: {video_url}")

    os.makedirs(output_dir, exist_ok=True)

    # Define output file names
    video_path = os.path.join(output_dir, "%(title)s_video.mp4")
    audio_path = os.path.join(output_dir, "%(title)s_audio.m4a")

    # Step 1: Download Video
    print("📥 Downloading video...")
    subprocess.run([
        "yt-dlp", "-f", "bestvideo[ext=mp4]", "-o", video_path, video_url
    ], check=True)

    # Step 2: Download Audio
    print("🎵 Downloading audio...")
    subprocess.run([
        "yt-dlp", "-f", "bestaudio[ext=m4a]", "-o", audio_path, video_url
    ], check=True)

    # Find the actual file names
    video_filename = find_downloaded_file(output_dir, "_video.mp4")
    audio_filename = find_downloaded_file(output_dir, "_audio.m4a")

    if not video_filename or not audio_filename:
        print("❌ Error: Could not find downloaded files.")
        return

    # Step 3: Merge Video & Audio
    print("🎬 Merging video and audio...")
    final_output = video_filename.replace("_video.mp4", ".mp4")
    subprocess.run([
        "ffmpeg", "-i", video_filename, "-i", audio_filename,
        "-c:v", "copy", "-c:a", "aac", "-strict", "experimental",
        final_output
    ], check=True)

    print(f"✅ Merging complete! Saved as: {final_output}")

    # Cleanup: Remove separate video/audio files
    os.remove(video_filename)
    os.remove(audio_filename)


def download_playlist(playlist_url, output_dir):
    """Download and merge all videos from a playlist."""
    print(f"\n📂 Downloading playlist: {playlist_url}")

    os.makedirs(output_dir, exist_ok=True)

    # Get all video URLs in the playlist
    result = subprocess.run(["yt-dlp", "--flat-playlist", "-J", playlist_url], capture_output=True, text=True,
                            check=True)
    playlist_data = eval(result.stdout)  # Convert JSON to Python dictionary

    for entry in playlist_data["entries"]:
        video_url = f"https://www.youtube.com/watch?v={entry['id']}"
        download_video(video_url, output_dir)


def find_downloaded_file(directory, suffix):
    """Find a file in the directory that ends with a specific suffix."""
    for file in os.listdir(directory):
        if file.endswith(suffix):
            return os.path.join(directory, file)
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YouTube videos or playlists and merge audio & video.")
    parser.add_argument("url", type=str, help="YouTube video or playlist URL")
    parser.add_argument("--output_dir", type=str, default="E:/download_video", help="Output directory")

    args = parser.parse_args()

    if "playlist?list=" in args.url:
        download_playlist(args.url, args.output_dir)
    else:
        download_video(args.url, args.output_dir)
