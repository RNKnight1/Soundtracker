import asyncio
import os
import sys
from shazamio import Shazam
from pydub import AudioSegment


async def main():
    if len(sys.argv) != 2:
        return
    filename, ext = os.path.splitext(sys.argv[1])
    shazam = Shazam()
    if ext == ".mp3":
        audio_segment = AudioSegment.from_mp3(sys.argv[1])
    elif ext == ".wav":
        audio_segment = AudioSegment.from_wav(sys.argv[1])
    else:
        return
    duration = audio_segment.duration_seconds * 1000
    slice_len = [0, 60000]
    while slice_len[1] < duration + 60000:
        audio_slice = audio_segment[slice_len[0] : slice_len[1]]
        slice_location = os.path.join(
            "temp", f"{filename} {slice_len[0]}-{slice_len[1]}{ext}"
        )
        audio_slice.export(slice_location, format=ext.replace(".", ""))
        out = await shazam.recognize_song(slice_location)
        if "track" in out.keys():
            print(f"{out['track']['subtitle']} - {out['track']['title']}")
        else:
            print("Not found")
            os.remove(slice_location)
        slice_len = [slice_len[0] + 60000, slice_len[1] + 60000]
        if slice_len[1] > duration and slice_len[1] != duration + 60000:
            slice_len[1] = duration


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
