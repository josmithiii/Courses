# `through-line.wav` — provenance & license

The shared through-line clip for the [`ai-music-audio`](../../ai-music-audio.md)
curriculum: one short solo-piano phrase carried, unchanged, across all three courses
(encode → tokenize → denoise).

## Source

- **Work:** Frédéric Chopin, *Waltz in A minor*, B. 150 (posthumous, "L'Adieu") —
  composition **public domain** (Chopin d. 1849).
- **Recording:** performed by **Aya Higuchi**, solo piano.
- **Source file:** `Chopin - Waltz in A minor, B 150.ogg` on Wikimedia Commons —
  https://commons.wikimedia.org/wiki/File:Chopin_-_Waltz_in_A_minor,_B_150.ogg
  (downloaded 2026-06-07; source is 2 min 10 s, stereo, 48 kHz Ogg Vorbis ~208 kb/s).

## License

**CC0 1.0 Universal — Public Domain Dedication**, for *both* the composition (age) and
this *recording* (the performer dedicated it CC0). Verbatim from the Commons page:

> "The person who associated a work with this deed has dedicated the work to the public
> domain by waiving all of their rights to the work worldwide under copyright law … You
> can copy, modify, distribute and perform the work, even for commercial purposes, all
> without asking permission."

So the clip is freely redistributable and may ship in this public repo. No attribution
is legally required; we record it here as good practice.

## What we ship vs. the source

`through-line.wav` is the **opening phrase** of the source recording, trimmed to ~2 s
and conditioned to the curriculum spec (mono, 24 kHz, 16-bit PCM):

| Field | Value |
|-------|-------|
| Duration | 2.200 s (52 800 samples) |
| Channels | mono |
| Sample rate | 24 000 Hz |
| Encoding | 16-bit PCM WAV |
| Level | peak-normalized to −1 dBFS |
| Window | 0.20 s → 2.40 s of the source (the opening melodic statement, ending at a natural gap) |

> Note: the source is lossy Ogg Vorbis, so the clip carries pre-existing Vorbis
> compression. That is fine — it's a 2-second pedagogical clip, not a reference master —
> but worth knowing when reading codec-reconstruction metrics in `audio-codecs`
> course 1 (the *relative* quality climb across `N_q` is what matters, not absolute SNR
> against a pristine original).

## Reproduce

```bash
# 1. Fetch the CC0 source from Wikimedia Commons
curl -L -A "CoursesLLM (educational)" -o chopin_b150.ogg \
  "https://upload.wikimedia.org/wikipedia/commons/f/f9/Chopin_-_Waltz_in_A_minor%2C_B_150.ogg"

# 2. Trim the opening phrase → mono 24 kHz 16-bit, with click-killing fades
ffmpeg -y -i chopin_b150.ogg -ss 0.20 -t 2.20 -ac 1 -ar 24000 \
  -af "afade=t=in:d=0.006,afade=t=out:st=2.10:d=0.10" -c:a pcm_s16le tl_raw.wav

# 3. Peak-normalize to -1 dBFS → through-line.wav
python3 - <<'PY'
import soundfile as sf, numpy as np
y, sr = sf.read("tl_raw.wav")
y = (y/np.max(np.abs(y))*10**(-1/20)).astype(np.float32)
sf.write("through-line.wav", (y*32767).astype(np.int16), sr, subtype='PCM_16')
PY
```
