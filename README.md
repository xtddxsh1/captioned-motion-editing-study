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

## Fixed-brief editing pilot — proposed USD 15

For tutorial creators and small teams with an existing editing reference and footage they are authorized to use: one finished clip of up to 30 seconds, in one agreed aspect ratio, assembled from up to five minutes of supplied footage/images.

Please supply the reference, the intended cut sequence or short brief, approved English caption text, and any licensed music you want included. The pilot covers basic cuts, sequencing, caption placement and the agreed MP4 export. New filming, new voiceover, custom illustration, stock purchases and native Premiere/After Effects/DaVinci projects are outside this offer.

**Delivery:** H.264/AAC MP4, an SRT file if captions are required, and the FFmpeg edit recipe with supporting source files. Acceptance checks are the agreed sequence/reference, approved caption text, dimensions, complete playback and successful decoding. One consolidated revision within the agreed scope is included.

**Timing and payment:** the proposed first review is within two working days of a jointly agreed start date, after the source material, permissions, scope, acceptance and payment arrangement are confirmed in writing. Proposed payment is USD 15 on written acceptance, within two business days. The actual payment method, Singapore eligibility, date and fees must be confirmed before production; no payment is collected through this repository.

For a current paid brief, email **xt20208022@gmail.com** with the target format, reference and approximate source duration. Do not put confidential footage, credentials or customer data in public issues. Files should be shared only through a mutually approved private channel after usage and confidentiality permission is established.

The pilot uses an AI-assisted Python/FFmpeg workflow; confirm that the supplied material may be processed with these tools. Commissioned files and usage rights are agreed separately from this study's MIT license.

The study above is self-initiated. Its original assets and source remain MIT licensed. This offer does not represent prior client experience, an accepted order or evidence of income.
