# Captioned motion editing study

An original 9-second portrait editing study made with Codex-assisted Python and FFmpeg. **Not game footage, a client project, a commercial portfolio history, or evidence of a paid order.**

Download [the MP4](./original-motion-editing-study.mp4?raw=true) or inspect the [source](./generate-study.py) and [captions](./captions.srt).

The result is 720 x 1280 at 30 fps, H.264 video / AAC audio, with hard cuts at 3 and 6 seconds. All 270 frames decoded successfully; nine actual decoded frames were checked for caption readability and clipping. It demonstrates this export and caption workflow only, not gameplay capture or voiceover accuracy.

Every shape, caption and mathematical sound cue is original. No client files, third-party footage or stock music are included. Original source and study assets are MIT licensed; system font files and third-party binaries are not distributed. Text is rasterized with Windows Segoe UI; font files are not embedded in the video.

## Reproduce

Use Python with Pillow and imageio-ffmpeg 0.6.0. On Windows with Segoe UI installed:

```powershell
python -m pip install --target tooling imageio-ffmpeg==0.6.0
python generate-study.py
```

The source writes output only within its own directory. Its font paths are Windows-specific; use a font you are licensed to use when adapting it to other systems. Third-party packages retain their own licenses.

## Scope

This is one reusable capability study. A commissioned clip requires an authorized brief and source material, agreed dimensions, price, acceptance, limited revisions, delivery date and payment terms before work begins. No performance or sales outcome is promised.
