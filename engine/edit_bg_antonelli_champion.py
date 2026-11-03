"""BG - F1: KIMI ANTONELLI, WORLD CHAMPION (Mexico City GP, Nov 1 2026 - the youngest champion ever) x "Apptekk" - lxao (#110,
the F1 sound of ref M29). Shape of U1/BF: the line builds over the quiet part, its payoff word IS the drop, then the hero on
every beat.
  0-3.7   "Max Verstappen is champion of the world." (2021 - F1's own name/age tag on screen)
  3.7-8.4 "Kimi Antonelli is the Formula One world -"   8.40 "CHAMPION" = the drop (song 11.01)
  8.4-14  champagne, the helmet, the flag, the team - a cut on every beat (0.627 s), ends on his face.
Footage: formula1.com official ("takes the crown", "title season in 60 seconds", podium celebration), 1280x720 50 fps,
native - no upscale. Shots with F1's own kinetic text ("CHAMPION", "YOUNGEST. EVER.", "SENSATIONAL") are not used."""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import wmtext
from edit_bf_spiderman_funk import glow_png

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ.get('DEX_MEX', os.path.join(S, 'mex'))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SONG = os.path.join(os.path.dirname(ROOT), 'dex-edits-assets', 'songs', '110_apptekk_lxao.mp3')
FPS = int(os.environ.get('DEX_FPS', 30))
W, H = 1280, 720
GRADE = 'eq=contrast=1.06:saturation=1.10'
F = {k: os.path.join(SRC, k + '.mp4') for k in ('crown', 'season60', 'celebrate')}
TALK = [(7.40, 11.10), (34.30, 39.00)]               # crown: commentary + picture in sync
PIC_LEAD = {1: 0.45}   # the Kimi call starts over the last Vettel frames: his picture starts 0.45 s later (commentary over)
DROP = sum(b - a for a, b in TALK)                   # 8.40
OFF = 11.012 - DROP
BEAT = lambda k: DROP + k * 0.6275
AFTER = [  # (beats, source, in-point, take end)
    (2, 'celebrate', 7.14, 8.92),    # champagne in his face
    (1, 'season60', 4.20, 5.40),     # the helmet (after F1's CHAMPION text)
    (1, 'season60', 47.42, 48.18),   # onboard
    (1, 'season60', 51.99, 52.62),   # the chequered flag
    (1, 'season60', 52.64, 53.34),   # green, white, red
    (1, 'season60', 42.12, 42.88),   # the champagne
    (1, 'season60', 56.02, 57.04),   # the team goes wild
    (1, 'season60', 58.80, 60.01),   # his face - the end
]
END = 16.70 - OFF
WORDS = [(7.52, 'MAX'), (7.94, 'VERSTAPPEN'), (8.60, 'IS'), (9.10, 'CHAMPION'), (9.70, 'OF'), (10.56, 'THE'), (10.78, 'WORLD.'),
         (34.38, '|KIMI'), (35.22, 'ANTONELLI'), (36.32, 'IS'), (36.88, 'THE'), (37.06, 'FORMULA'), (37.50, 'ONE'), (38.18, 'WORLD')]


def edit_t(src_t):
    e = 0.0
    for a, b in TALK:
        if a <= src_t <= b: return e + src_t - a
        e += b - a
    raise ValueError(src_t)


def captions():
    out, line = [], []
    for i, (t, w) in enumerate(WORDS):
        if w.startswith('|'): line = []; w = w[1:]
        line.append(w)
        nxt = WORDS[i + 1] if i + 1 < len(WORDS) else None
        end = DROP - 0.001 if nxt is None else (edit_t(TALK[0][1]) - 0.001 if nxt[1].startswith('|') else edit_t(nxt[0]))
        out.append((edit_t(t), end, ' '.join(line)))
    return out


def render(out):
    tmp = os.path.join(S, 'tmp_bg'); os.makedirs(tmp, exist_ok=True)
    parts, t = [], 0.0
    def clip(k, s, d, name):
        n = round((t + d) * FPS) - round(t * FPS); p = os.path.join(tmp, name)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{s:.3f}', '-i', F[k], '-frames:v', str(n), '-an', '-vf',
                        f'fps={FPS},{GRADE},setsar=1', '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-pix_fmt', 'yuv420p', p], check=True)
        parts.append(p)
    for i, (a, b) in enumerate(TALK):
        clip('crown', a + PIC_LEAD.get(i, 0), b - a, f'a{i}.mp4'); t += b - a
    for i, (n, k, s, e) in enumerate(AFTER):
        d = (BEAT(sum(x for x, *_ in AFTER[:i + 1])) if i + 1 < len(AFTER) else END) - t
        assert s + d <= e + 0.03, f'after #{i} runs past its take ({s + d:.2f} > {e})'
        clip(k, s, d, f'b{i:02d}.mp4'); t += d
    lst = os.path.join(tmp, 'list.txt'); open(lst, 'w').write(''.join(f"file '{x}'\n" for x in parts))
    vid = os.path.join(tmp, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid], check=True)

    words = captions()
    import edit_bf_spiderman_funk as bf
    bf.W, bf.H = W, H                                   # glow_png draws on this frame size
    pngs = [glow_png(w, os.path.join(tmp, f'c{i:02d}.png'), size=44, cy=0.55) for i, (_, _, w) in enumerate(words)]   # above F1's own name tag
    pngs.append(wmtext.word_png('WORLD CHAMPION.', W, H, os.path.join(tmp, 'big.png'), size=int(H * 0.13)))
    texts = words + [(DROP, BEAT(2) - 0.02, 'WORLD CHAMPION.')]
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', vid, '-ss', f'{OFF:.3f}', '-i', SONG]
    for p in pngs: cmd += ['-loop', '1', '-framerate', str(FPS), '-t', f'{END:.3f}', '-i', p]
    chain, last = wmtext.overlay_filter(texts, 2, '[0:v]')
    n0 = 2 + len(pngs); fx, labels, e = '', [], 0.0
    for i, (a, b) in enumerate(TALK):             # the commentators, in sync with their pictures; the last runs through "CHAMPION"
        tail = 0.65 if i == len(TALK) - 1 else 0.0
        cmd += ['-ss', f'{a:.3f}', '-t', f'{b - a + tail:.3f}', '-i', F['crown']]
        fx += (f"[{n0 + i}:a]aformat=channel_layouts=stereo,highpass=f=90,afade=t=in:d=0.03,afade=t=out:st={b - a + tail - 0.15:.3f}:d=0.15,"
               f"volume=1.8,adelay={int(e * 1000)}|{int(e * 1000)}[v{i}];")
        labels.append(f'[v{i}]'); e += b - a
    fx += (f"[1:a]atrim=0:{END:.3f},asetpts=PTS-STARTPTS,volume='if(lt(t,{DROP - 0.04:.3f}),0.35,1.0)':eval=frame,"
           f"afade=t=out:st={END - 0.4:.3f}:d=0.4[song];[song]{''.join(labels)}amix=inputs={len(labels) + 1}:normalize=0,alimiter=limit=0.85[a]")
    subprocess.run(cmd + ['-filter_complex', chain + fx, '-map', last, '-map', '[a]', '-t', f'{END:.3f}', '-r', str(FPS),
                          '-c:v', 'libx264', '-crf', '12', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', out], check=True)
    print(out, f'drop {DROP:.2f} end {END:.2f}')


if __name__ == '__main__':
    render(os.path.join(S, 'out', f'bg_antonelli_{FPS}.mp4'))
