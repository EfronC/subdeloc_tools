# Subtitle Delocalizer Tools
----------------------------

## SubTools

Main class

## Modules

### Extract Subs

Extract subtitle file from an MKV based on the index or the lang(Requires FFMPEG)

### Merger

Mux/Demux subs from an MKV file

### Shift Subs

Shift subtitles a determined amount of seconds. Allows to choose a threshold to choose from which point to shift.

### Pair subs

Pair 2 subtitle file subs based on the time

### Honorific Fixer

Receives a PairSubtitles JSON, and an ASS file used to generate it, and creates a new ASS file with the modified subs

```
[
  {
    "start": 0,
    "end": 12250,
    "reference": [
      {
        "start": 0,
        "end": 12180,
        "text": "こんにちは世界",
        "nl": 1
      }
    ],
    "original": [
      {
        "start": 1000,
        "end": 12250,
        "text": "Hello World",
        "nl": 1
      }
    ]
  },
  ...
]
```