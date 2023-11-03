# Soundtracker
Shazam tracks from audio files of totally legally obtained movies or episodes.

Requires [FFmpeg](https://ffmpeg.org/download.html)

        git clone https://github.com/RNKnight1/Soundtracker.git
        cd Soundtracker

[vocal-remover](https://github.com/tsurumeso/vocal-remover) can be used to remove vocals from audio files.

        python extract_audio.py [video_file]

to extract audio from video files

        python record.py [length] -t [title] -e [episode (S1E1)]

to record audio

        python main.py [audio_file]