# Subtitle Delocalizer Tools
----------------------------

## SubTools

Main class

Common usage
```
res = pairsubs.pair_files("main_subtitle.ass", "japanese_reference.ass") # Generates PairSubtitles JSON
s = self.search_honorifics(res) # Modify texts in the PairSubtitles JSON, adding the required honorifics
honorific_fixer.fix_original("main_subtitle.ass", s) # Generates a new ASS file with updated subtitles
```

## Modules

### Extract Subs

Extract subtitle file from an MKV based on the index or the lang(Requires FFMPEG). Extracts both ASS and SRT subtitles.

```
from subdeloc_tools.modules import extract_subs

generated_filename = extract_subs_by_lang("subtitle.ass", "eng")
generated_filename = extract_subs_by_index("subtitle.srt", 1)
```

### Merger

Mux/Demux subs from an MKV file.

```
from .merger import Merger

merger = Merger()
merger.set_file("subtitle.mkv")
streams = merger.get_streams()
index = merger.get_language_index("en")
generated_filename = merger.demux("subtitle.mkv", index, "output.ass")
```

### Shift Subs

Shift subtitles a determined amount of seconds. Allows to choose a threshold to choose from which point to shift.

```
from subdeloc_tools.modules import shift_subs

generated_filename = shift_sub("subtitle.ass", 10, 102900) # Shift 10 seconds from 00:01:42
generated_filename = shift_sub("subtitle.ass", 10, 0) # Shift 10 seconds all subs
```

### Pair subs

Pair 2 subtitle file subs based on the time. Generates a PairSubtitles JSON

```
from subdeloc_tools.modules import pairsubs

res = pairsubs.pair_files("main_subtitle.ass", "japanese_reference.ass")
```

### Honorific Fixer

Receives a PairSubtitles JSON, and an ASS file used to generate it, and creates a new ASS file with the modified subs

```
from subdeloc_tools.modules import honorific_fixer

honorific_fixer.fix_original("main_subtitle.ass", s)
```

## Glossary

PairSubtitles JSON
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

Sister projects:
- [C Tools](https://github.com/EfronC/subdeloc_helper)
- [Delocalizer](https://github.com/EfronC/Delocalizer)