import subprocess
import os
import sys


def convert_video_to_audio_ffmpeg(video_file, output_ext="mp3"):
    """Converts video to audio directly using `ffmpeg` command
    with the help of subprocess module"""
    filename, ext = os.path.splitext(video_file)
    if not os.path.exists(video_file) or not os.path.isfile(video_file):
        video_file = os.path.join("video", video_file)
    subprocess.call(
        [
            "ffmpeg",
            "-y",
            "-i",
            video_file,
            os.path.join("audio", f"{filename}.{output_ext}")
            if os.path.exists("audio")
            else f"{filename}.{output_ext}",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )


if __name__ == "__main__" and len(sys.argv) == 2:
    vf = sys.argv[1]
    convert_video_to_audio_ffmpeg(vf)
