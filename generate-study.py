"""Original code-drawn motion/editing study. No client or game footage."""
from pathlib import Path
import hashlib
import json
import math
import re
import struct
import subprocess
import sys
import wave

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tooling'))
import imageio_ffmpeg

W, H, FPS, DURATION = 720, 1280, 30, 9
FRAME_COUNT = FPS * DURATION
SCALE = 1.5
RW, RH = int(W * SCALE), int(H * SCALE)
FONT_REG = Path('C:/Windows/Fonts/segoeui.ttf')
FONT_BOLD = Path('C:/Windows/Fonts/segoeuib.ttf')
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
WHITE = '#F4F5F0'
INK = '#10182A'
CYAN = '#76E8D5'
CORAL = '#FF846C'
LIME = '#E9EDAA'

def font(size, bold=False):
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REG), round(size * SCALE))

def xy(points):
    return tuple(round(v * SCALE) for v in points)

def text(draw, at, content, size, color=WHITE, bold=False, anchor=None):
    draw.text(xy(at), content, font=font(size, bold), fill=color, anchor=anchor)

def rounded(draw, box, fill, radius=18, outline=None, width=1):
    draw.rounded_rectangle(xy(box), radius=round(radius * SCALE), fill=fill,
                           outline=outline, width=round(width * SCALE))

def ellipse(draw, box, fill=None, outline=None, width=1):
    draw.ellipse(xy(box), fill=fill, outline=outline, width=round(width * SCALE))

def line(draw, points, fill, width=1):
    draw.line([xy(p) for p in points], fill=fill, width=round(width * SCALE), joint='curve')

def blend(a, b, p):
    return tuple(round(a[i] * (1-p) + b[i] * p) for i in range(3))

def background(top, bottom):
    im = Image.new('RGB', (RW, RH))
    d = ImageDraw.Draw(im)
    for y in range(RH):
        d.line((0, y, RW, y), fill=blend(top, bottom, y / (RH-1)))
    return im

BASES = [background((13, 25, 42), (26, 47, 62)),
         background((237, 113, 91), (251, 149, 117)),
         background((12, 23, 39), (29, 43, 56))]
CAPTIONS = ['Start with a clear hook.', 'Cut straight to the action.',
            'Keep the message readable.']
CAPTION_TIMES = [(0.25, 3.0), (3.0, 6.0), (6.0, 9.0)]
TITLES = [('Find the', 'first beat.'), ('Make the', 'cut count.'), ('Leave a', 'clear idea.')]

def render_frame(t):
    scene = min(int(t / 3), 2)
    local = t - 3 * scene
    im = BASES[scene].copy()
    d = ImageDraw.Draw(im)
    fg = INK if scene == 1 else WHITE
    muted = '#542D2C' if scene == 1 else '#ACBECA'
    accent = INK if scene == 1 else CYAN
    # Persistent provenance label: the clip is an editing exercise, never a game claim.
    text(d, (44, 38), 'ORIGINAL MOTION / EDITING STUDY', 18, fg, True)
    line(d, [(44, 80), (676, 80)], '#B15A4C' if scene == 1 else '#405261', 1)
    text(d, (44, 112), f'0{scene+1}', 24, accent, True)
    text(d, (94, 113), ['HOOK', 'ACTION', 'CLARITY'][scene], 21, muted, True)
    text(d, (44, 176), TITLES[scene][0], 73, fg, True)
    text(d, (44, 263), TITLES[scene][1], 73, fg, True)

    if scene == 0:
        # A moving circle follows a visibly hand-authored geometric route.
        points = [(110 + 500*i/80, 740 - 105*math.sin(i/80*math.pi)) for i in range(81)]
        line(d, points, '#3A6072', 3)
        for x, y in [(110, 740), (360, 635), (610, 740)]:
            ellipse(d, (x-8, y-8, x+8, y+8), LIME)
        p = 0.5 - 0.5 * math.cos(local/3*math.pi)
        x, y = 110+500*p, 740-105*math.sin(p*math.pi)
        r = 51 + 4*math.sin(local*math.pi*2)
        ellipse(d, (x-r-13, y-r-13, x+r+13, y+r+13), outline='#407A86', width=2)
        ellipse(d, (x-r, y-r, x+r, y+r), CYAN)
        ellipse(d, (x-15, y-16, x+8, y+7), INK)
        rounded(d, (44, 870, 270, 914), '#243E4E', 22)
        text(d, (64, 879), 'One moving focal point', 17, WHITE)
    elif scene == 1:
        # Hard cut to a close crop with quick diagonal movement.
        rounded(d, (44, 480, 676, 926), INK, 32)
        for offset in range(5):
            y = 550 + offset*70
            line(d, [(85, y), (634, y-45)], '#30465A', 2)
        p = (local/3)
        x = 190 + 350*(0.5-0.5*math.cos(p*math.pi))
        y = 747 - 90*math.sin(p*math.pi*1.5)
        for i in range(4, 0, -1):
            rr = 70 - i*7
            ellipse(d, (x-rr-i*35, y-rr+i*8, x+rr-i*35, y+rr+i*8), '#30465A')
        ellipse(d, (x-90, y-90, x+90, y+90), LIME)
        ellipse(d, (x-34, y-30, x+15, y+19), INK)
        # Visual cut mark, rather than a logo or a pretend game UI.
        line(d, [(586, 820), (616, 790), (643, 817)], CORAL, 7)
    else:
        # The same visual vocabulary resolves to three calm, readable beats.
        for i, color in enumerate([CYAN, CORAL, LIME]):
            x = 148 + i*212
            pulse = 1 + 0.075*math.sin(local*math.pi*2 - i*0.9)*math.exp(-local/2)
            r = 72*pulse
            ellipse(d, (x-r-9, 700-r-9, x+r+9, 700+r+9), outline='#45596B', width=2)
            ellipse(d, (x-r, 700-r, x+r, 700+r), color)
            if i == 0:
                d.polygon([xy((x-18, 676)), xy((x-18, 724)), xy((x+22, 700))], fill=INK)
            elif i == 1:
                line(d, [(x-20, 676), (x+20, 724)], INK, 8)
                line(d, [(x+20, 676), (x-20, 724)], INK, 8)
            else:
                line(d, [(x-25, 699), (x-6, 718), (x+29, 681)], INK, 8)
        text(d, (360, 853), 'A short sequence. A clear message.', 22, '#BACAD4', anchor='mm')

    # Burned captions remain inside generous portrait safe margins.
    if t >= CAPTION_TIMES[scene][0]:
        rounded(d, (36, 988, 684, 1078), '#F4F5F0', 18)
        text(d, (360, 1030), CAPTIONS[scene], 31, INK, True, anchor='mm')
    # Scene progress and disclaimer are visible at all cuts.
    for i in range(3):
        rounded(d, (44+i*214, 1135, 44+i*214+198, 1141),
                accent if i <= scene else ('#B15A4C' if scene == 1 else '#405261'), 3)
    text(d, (44, 1190), 'Not game footage or a client project.', 20, fg)
    return im.resize((W, H), Image.Resampling.LANCZOS)

def write_audio():
    # Original mathematical tones: no music library, voice, or third-party audio.
    rate = 48000
    data = bytearray()
    for n in range(rate * DURATION):
        t = n / rate
        v = 0.0
        for start, freq in [(0.15, 392), (3.03, 523.251), (6.03, 659.255)]:
            dt = t-start
            if 0 <= dt < 0.32:
                envelope = (1-math.exp(-dt*200))*math.exp(-dt*15)
                v += 0.16*envelope*(math.sin(2*math.pi*freq*dt)+0.16*math.sin(2*math.pi*2*freq*dt))
        data.extend(struct.pack('<h', int(max(-1, min(1, v))*32767)))
    audio = ROOT / 'original-tones.wav'
    with wave.open(str(audio), 'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(rate); f.writeframes(data)
    return audio

def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    audio = write_audio()
    out = ROOT / 'original-motion-editing-study.mp4'
    command = [FFMPEG, '-y', '-hide_banner', '-loglevel', 'error',
               '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
               '-i', '-', '-i', str(audio), '-t', str(DURATION),
               '-c:v', 'libx264', '-preset', 'fast', '-crf', '20', '-pix_fmt', 'yuv420p',
               '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart',
               '-metadata', 'title=Original motion/editing study',
               '-metadata', 'comment=Not game footage or a client project. Original code-drawn shapes and synthesized tones.',
               str(out)]
    with (ROOT / 'encode.log').open('w', encoding='utf-8') as log:
        proc = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=log)
        try:
            for i in range(FRAME_COUNT):
                proc.stdin.write(render_frame(i/FPS).tobytes())
            proc.stdin.close()
        except Exception:
            proc.kill(); proc.wait(); raise
        if proc.wait() != 0:
            raise RuntimeError('Encoding failed; see encode.log')
    subtitles = '1\n00:00:00,250 --> 00:00:03,000\nStart with a clear hook.\n\n2\n00:00:03,000 --> 00:00:06,000\nCut straight to the action.\n\n3\n00:00:06,000 --> 00:00:09,000\nKeep the message readable.\n'
    (ROOT / 'captions.srt').write_text(subtitles, encoding='utf-8')
    version = subprocess.run([FFMPEG, '-version'], capture_output=True, text=True, check=True).stdout
    probe = subprocess.run([FFMPEG, '-hide_banner', '-i', str(out)], capture_output=True, text=True)
    (ROOT / 'probe.txt').write_text(probe.stderr, encoding='utf-8')
    decode = subprocess.run([FFMPEG, '-hide_banner', '-i', str(out), '-map', '0:v:0',
                             '-f', 'null', '-'], capture_output=True, text=True, check=True)
    (ROOT / 'decode-validation.txt').write_text(decode.stderr, encoding='utf-8')
    # Extract real decoded frames from the MP4, including both sides of each cut.
    frame_dir = ROOT / 'decoded-frames'
    frame_dir.mkdir(exist_ok=True)
    times = [0.0, 0.6, 2.9, 3.0, 4.5, 5.9, 6.0, 7.5, 8.9]
    frame_paths = []
    for t in times:
        target = frame_dir / f'frame-{t:04.1f}s.png'
        subprocess.run([FFMPEG, '-y', '-hide_banner', '-loglevel', 'error', '-ss', str(t),
                        '-i', str(out), '-frames:v', '1', str(target)], check=True)
        frame_paths.append(target)
    contact = Image.new('RGB', (3*240, 3*460), '#080E18')
    cd = ImageDraw.Draw(contact)
    tiny = ImageFont.truetype(str(FONT_REG), 18)
    for i, (t, p) in enumerate(zip(times, frame_paths)):
        col, row = i%3, i//3
        with Image.open(p) as fr:
            fr.thumbnail((240, 427))
            contact.paste(fr, (col*240, row*460+28))
        cd.text((col*240+8, row*460+4), f'{t:.1f}s', font=tiny, fill=WHITE)
    contact.save(ROOT / 'contact-sheet.png')
    info = {
        'label': 'Original motion/editing study; not game footage or a client project',
        'output': str(out), 'duration_s_requested': DURATION, 'fps_requested': FPS,
        'dimensions': [W,H], 'aspect_ratio': '9:16', 'frames_generated': FRAME_COUNT,
        'codec_requested': 'H.264 / AAC', 'burned_captions': True,
        'cut_times_s': [3.0,6.0], 'caption_times_s': CAPTION_TIMES,
        'audio': 'Original synthesized soft tones, no voiceover or third-party music',
        'all_artwork': 'Original Python/Pillow code-drawn geometric shapes; no external imagery or game footage',
        'fonts': 'System Segoe UI, font binaries not redistributed',
        'ffmpeg_binary': FFMPEG, 'ffmpeg_version': version.splitlines()[0],
        'encoding_command': command, 'probe_command': [FFMPEG,'-hide_banner','-i',str(out)],
        'probe_expected_exit': 'ffmpeg -i alone exits 1 because no output is specified; probe metadata remains valid',
        'decode_exit_code': decode.returncode,
        'decoded_video_frame_count': int(re.findall(r'frame=\s*(\d+)', decode.stderr)[-1]),
        'decoded_frame_times_s': times, 'decoded_frames': [str(p) for p in frame_paths],
        'output_bytes': out.stat().st_size,
        'sha256': hashlib.sha256(out.read_bytes()).hexdigest(),
        'cash_spent': 0,
        'limitations': ['No actual gameplay capture or client work is shown',
                       'No voiceover understanding is demonstrated',
                       'No claim of professional editing experience',
                       'Not published or submitted to any employer']
    }
    (ROOT / 'render-manifest.json').write_text(json.dumps(info, indent=2), encoding='utf-8')
    print(json.dumps({'output': str(out), 'bytes': out.stat().st_size,
                      'frames': info['decoded_video_frame_count'], 'decode_ok': True}))

if __name__ == '__main__':
    main()
