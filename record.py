import argparse
import os

# import required libraries
import sounddevice as sd
import wavio as wv


def convert_time_to_seconds(time_str):
    try:
        nums = time_str.split(":")
        if len(nums) == 1 and nums[0].isnumeric():
            return int(nums[0])
        elif len(nums) == 2:
            return int(nums[0]) * 60 + int(nums[1])
        elif len(nums) == 3:
            return int(nums[0]) * 3600 + int(nums[1]) * 60 + int(nums[2])
        else:
            raise ValueError("Invalid time format. Use HH:MM:SS, MM:SS, or seconds.")
    except ValueError as e:
        raise ValueError(f"Error: {e}") from e


def record_audio(args):
    duration = convert_time_to_seconds(args.length)
    if args.title:
        title = args.title
        if args.episode:
            title = f"{title} S{args.episode[0]}E{args.episode[1]}"
    freq = 44100
    # Start recorder with the given values of
    # duration and sample frequency
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)

    # Record audio for the given number of seconds
    sd.wait()
    # Convert the NumPy array to audio file
    wv.write(
        os.path.join("audio", f"{title}.wav" if title else "recording.wav"),
        recording,
        freq,
        sampwidth=2,
    )


def main():
    parser = argparse.ArgumentParser(
        prog="Soundtracker",
        description="Finds the name of the track from the soundtrack based on audio file or recording.",
        epilog="Text at the bottom of help",
    )
    parser.add_argument(
        "length", help="Time duration in the format HH:MM:SS, MM:SS, or seconds"
    )
    parser.add_argument("-t", "--title", help="Title for movie or series")
    parser.add_argument(
        "-e",
        "--episode",
        type=int,
        nargs=2,
        help="Episode number in the format season episode",
    )
    args = parser.parse_args()

    try:
        record_audio(args)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
