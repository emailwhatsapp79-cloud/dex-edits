"""BA - Kane, 'from fan to captain' (one-story, VERTICAL native 1080x1920 - official @fifaworldcup clips, filmed
vertical; nothing cropped or scaled). Kane's own words on his first World Cup memory (studio, lip-synced, sharpest shot
first) -> hard cut on the song to his 2026 goal and shirt-pull celebration; 'just keep watchin'' (#72, Desmond: re-use
this song) lands on the celebration."""
import os, subprocess, sys

S = os.environ.get('SCRATCH', '/tmp')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.environ.get('DEX_ASSETS', os.path.join(os.path.dirname(ROOT), 'dex-edits-assets'))
TALK = os.path.join(S, 'src_kane', 'fifaworldcup_7646705250455276803.mp4')
GOAL = os.path.join(S, 'src_kane', 'fifaworldcup_7657694274565213462.mp4')
SONG = os.path.join(ASSETS, 'songs', '72_f1_60s_edit_cs_ttzz.mp3')
FONT = os.path.join(ROOT, 'fonts', 'Anton.ttf')
SHOTS = [(TALK, 25.40, 4.60), (GOAL, 17.60, 2.60), (GOAL, 21.90, 0.70), (GOAL, 26.00, 5.00)]   # (src, in, dur)
SONG_AT_0 = 1.42           # song time at edit 0 -> 'just keep watchin'' (song 9.62) lands at edit 8.2
VOICE_END = 4.60
TEXT = [(0.05, 4.55, "2002.|HE WAS THE FAN|WATCHING ON A SCHOOL TV", 92, 0.20),
        (4.62, 7.15, '2026.', 150, 0.22),
        (8.10, 12.90, 'NOW ENGLAND|WATCHES HIM.', 110, 0.20)]


def dt(t0, t1, text, fs, y):
    lines = text.split('|'); out = ''
    for i, l in enumerate(lines):
        l = l.replace("'", '’').replace(':', '\\:').replace(',', '\\,')
        out += (f",drawtext=fontfile={FONT}:text='{l}':fontsize={fs}:fontcolor=white:borderw=3:bordercolor=black@0.45:"
                f"shadowcolor=black@0.55:shadowy=4:x=(w-text_w)/2:y=h*{y}+{i}*{int(fs * 1.12)}:enable='between(t,{t0},{t1})'")
    return out


def main():
    os.makedirs(os.path.join(S, 'out'), exist_ok=True)
    inp, fc, cat = [], '', ''
    for i, (src, a, d) in enumerate(SHOTS):
        inp += ['-ss', f'{a}', '-t', f'{d}', '-i', src]
        fc += f'[{i}:v]fps=30,setpts=PTS-STARTPTS,setsar=1[v{i}];'; cat += f'[v{i}]'
    end = sum(d for _, _, d in SHOTS); n = len(SHOTS)
    fc += f'{cat}concat=n={n}:v=1:a=0[vc];[vc]null' + ''.join(dt(*t) for t in TEXT) + '[v];'
    inp += ['-ss', f'{SONG_AT_0}', '-i', SONG]
    fc += (f"[0:a]atrim=0:{VOICE_END},asetpts=PTS-STARTPTS,volume=1.6,apad=whole_dur={end}[voice];"
           f"[{n}:a]atrim=0:{end},asetpts=PTS-STARTPTS,volume='if(lt(t,{VOICE_END}),0.12,1)':eval=frame,"
           f"afade=t=out:st={end - 0.7}:d=0.7[song];[voice][song]amix=inputs=2:duration=longest:normalize=0[a]")
    out = os.path.join(S, 'out', 'ba_kane_fan.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-t', f'{end}',
                    '-c:v', 'libx264', '-crf', '10', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', out], check=True)
    sys.path.insert(0, os.path.dirname(__file__)); import brand
    print(brand.brand(out, out.replace('.mp4', '_DEX.mp4')))


if __name__ == '__main__':
    main()
