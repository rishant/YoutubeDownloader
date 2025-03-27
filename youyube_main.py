import os
import subprocess
import argparse


def download_video(video_url, output_dir, quality):
    """Download a single video with selected quality and merged audio."""
    print(f"\n🔹 Downloading: {video_url} with quality: {quality}")

    os.makedirs(output_dir, exist_ok=True)

    # Define the output file format with quality included
    output_path = os.path.join(output_dir, "%(title)s_" + quality + ".%(ext)s")

    # Select format based on quality
    quality_map = {
        "best": "bv+ba/best",
        "1080p": "bestvideo[height<=1080]+bestaudio/best",
        "720p": "bestvideo[height<=720]+bestaudio/best",
        "480p": "bestvideo[height<=480]+bestaudio/best",
        "360p": "bestvideo[height<=360]+bestaudio/best",
        "240p": "bestvideo[height<=240]+bestaudio/best"
    }

    format_string = quality_map.get(quality, "bv+ba/best")

    # Download video
    subprocess.run([
        "yt-dlp", "-f", format_string, "-o", output_path, video_url
    ], check=True)

    print(f"✅ Download complete! Saved to: {output_dir}")


def download_playlist(playlist_url, output_dir, quality):
    """Download all videos in a playlist with selected quality and merged audio."""
    print(f"\n📂 Downloading playlist: {playlist_url} with quality: {quality}")

    os.makedirs(output_dir, exist_ok=True)

    # Define output format with quality included
    output_path = os.path.join(output_dir, "%(title)s_" + quality + ".%(ext)s")

    # Select format based on quality
    quality_map = {
        "best": "bv+ba/best",
        "1080p": "bestvideo[height<=1080]+bestaudio/best",
        "720p": "bestvideo[height<=720]+bestaudio/best",
        "480p": "bestvideo[height<=480]+bestaudio/best",
        "360p": "bestvideo[height<=360]+bestaudio/best",
        "240p": "bestvideo[height<=240]+bestaudio/best"
    }

    format_string = quality_map.get(quality, "bv+ba/best")

    # Download playlist
    subprocess.run([
        "yt-dlp", "-f", format_string, "-o", output_path,
        "--yes-playlist", playlist_url
    ], check=True)

    print(f"✅ Playlist downloaded successfully in: {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YouTube videos or playlists with selected quality.")
    parser.add_argument("url", type=str, help="YouTube video or playlist URL")
    parser.add_argument("--output_dir", type=str, default="E:/download_video", help="Output directory")
    parser.add_argument("--quality", type=str, choices=["best", "1080p", "720p", "480p", "360p", "240p"],
                        default="best", help="Video quality (default: best)")

    args = parser.parse_args()

    if "playlist?list=" in args.url:
        download_playlist(args.url, args.output_dir, args.quality)
    else:
        download_video(args.url, args.output_dir, args.quality)
