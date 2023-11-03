import asyncio
import os
import sys
from shazamio import Shazam
from pydub import AudioSegment


async def main():
    if len(sys.argv) != 2:
        return
    if not os.path.exists(sys.argv[1]):
        print("File not found")
        return
    file_location = os.path.split(sys.argv[1])
    filename, ext = os.path.splitext(file_location[-1])
    # timestamps = []
    if os.path.exists("timestamps"):
        timestamp_loc = os.path.join("timestamps", f"{filename}.txt")
    else:
        timestamp_loc = os.path.join(*file_location[:-1], f"{filename}.txt")
    shazam = Shazam()
    audio_segment = AudioSegment.from_file(sys.argv[1], ext.replace(".", ""))
    duration = audio_segment.duration_seconds * 1000
    slice_len = [0, 60000]
    tracks = {}
    while slice_len[1] < duration + 60000:
        audio_slice = audio_segment[slice_len[0] : slice_len[1]]
        slice_location = os.path.join(
            *file_location[:-1],
            "temp",
            f"{int(slice_len[0] / 1000)}-{int(slice_len[1] / 1000)} {file_location[-1]}",
        )
        audio_slice.export(slice_location, format=ext.replace(".", ""))
        out = await shazam.recognize_song(slice_location)
        if "track" in out.keys():
            if (
                f"{out['track']['subtitle']} - {out['track']['title']}"
                not in tracks.values()
            ):
                print(f"{out['track']['subtitle']} - {out['track']['title']}")
                tracks[
                    f"{int(slice_len[0] / 60000)}:00-{int(slice_len[1] / 60000)}:00"
                ] = f"{out['track']['subtitle']} - {out['track']['title']}"
            else:
                if (
                    list(tracks.values()).index(
                        f"{out['track']['subtitle']} - {out['track']['title']}"
                    )
                    == len(tracks.values()) - 1
                ):
                    timestamps = list(tracks.keys())[
                        list(tracks.values()).index(
                            f"{out['track']['subtitle']} - {out['track']['title']}"
                        )
                    ].split("-")
                    tracks[
                        f"{timestamps[0]}-{int(slice_len[1] / 60000)}:00"
                    ] = f"{out['track']['subtitle']} - {out['track']['title']}"
                    tracks.pop("-".join(timestamps))
                # timestamps.append(f"{int(slice_len[0] / 60000)}:00: {out['track']['subtitle']} - {out['track']['title']}")
        else:
            print(
                f"{int(slice_len[0] / 60000)}:00-{int(slice_len[1] / 60000)}:00 Not found"
            )
        os.remove(slice_location)
        slice_len = [slice_len[0] + 60000, slice_len[1] + 60000]
        if slice_len[1] > duration and slice_len[1] != duration + 60000:
            slice_len[1] = duration
    with open(timestamp_loc, "w") as timetext:
        text = "".join(f"{key}: {value}\n" for key, value in tracks.items())
        timetext.write(text)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
