import os
import subprocess
import argparse


def download_video(video_url, output_dir):
    """Download a single video with merged audio."""
    print(f"\n🔹 Downloading: {video_url}")

    os.makedirs(output_dir, exist_ok=True)

    # Define the output file format
    output_path = os.path.join(output_dir, "%(title)s.mp4")

    # Download best video+audio format in one go
    subprocess.run([
        "yt-dlp", "-f", "bv+ba", "-o", output_path, video_url
    ], check=True)

    print(f"✅ Download complete! Saved to: {output_dir}")


def download_playlist(playlist_url, output_dir):
    """Download all videos in a playlist with merged audio."""
    print(f"\n📂 Downloading playlist: {playlist_url}")

    os.makedirs(output_dir, exist_ok=True)

    # Download all videos in playlist
    subprocess.run([
        "yt-dlp", "-f", "bv+ba", "-o", os.path.join(output_dir, "%(title)s.mp4"),
        "--yes-playlist", playlist_url
    ], check=True)

    print(f"✅ Playlist downloaded successfully in: {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YouTube videos or playlists with merged audio.")
    parser.add_argument("url", type=str, help="YouTube video or playlist URL")
    parser.add_argument("--output_dir", type=str, default="E:/download_video", help="Output directory")

    args = parser.parse_args()

    if "playlist?list=" in args.url:
        download_playlist(args.url, args.output_dir)
    else:
        download_video(args.url, args.output_dir)
