#! /bin/bash

# Dumps default audio to pcm-coded 16-bit mono
ffmpeg -f \
    pulse,name=SpeechRecognition,stream_name=listen,channels=1,sample_rate=16000 \
    -ac 1 -ar 16000 -f s16le -acodec pcm_s16le pipe:1 >  /tmp/dspipe/audio
