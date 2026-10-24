"""BD - F1: "YOU READY?" - Lap 1 of the 2026 season, cut like ref K1 (@kam_cuts, 1.4M): same sound (#133), the cut map of
the reference (its editor already placed every cut on a music event), and the ACTION inside each shot - a car passing the
lens, a start launch, a lock-up, cars touching - fitted onto the sound inside that shot (engine/actionsync.fit).
Hook: start lights + "YOU / READY?" (watermark lyrics, Desmond Oct 23). Payoff "LAP 1. / IS WAR." on the breath (12.96),
end "AUSTIN. / YOU READY?". Footage: official formula1.com 2026 race highlights, LAP 1 only (no timing tower yet);
every frame cropped just below the LAP 1/xx box (1070x602 of 1280x720, kept native - no upscale).
Usage: python3 edit_bd_lap1_ready.py [fit|stills|render] ; DEX_FPS=50 for the YouTube master."""
import os, sys, json, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import actionsync, wmtext

S = os.environ.get('SCRATCH', '/tmp')
O = os.environ.get('DEX_F1', '/tmp/claude-0/-home-user-scamdecoded-media/7be1f147-2656-5ce6-9a44-2202ae528a61/scratchpad')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SONG = os.path.join(os.path.dirname(ROOT), 'dex-edits-assets', 'songs', '133_k1_kam_cuts_another_banger_anime.mp3')
FPS = int(os.environ.get('DEX_FPS', 30))
W, H, X0, Y0 = 1070, 602, 105, 118          # crop below the LAP box, native pixels
GRADE = 'eq=contrast=1.08:saturation=1.10:gamma=0.96'
F = {'monaco': f'{O}/dl_gs/monaco.mp4', 'monza': f'{O}/dl_gs/monza.mp4', 'baku': f'{O}/dl_gs/baku.mp4',
     'dutch': f'{O}/dl_gs/dutch.mp4', 'austria': f'{O}/dl_gs/austria.mp4', 'sing': f'{O}/dl_f1sg/f1web_1878763614925929557.mp4'}

# the reference's cut map (ref K1, measured), up to the end card
CUTS = [0, 1.333, 1.667, 2.042, 2.375, 2.792, 3.125, 3.542, 3.708, 4.750, 4.917, 5.292, 5.458, 5.750, 5.917, 7.333, 7.750,
        7.917, 8.083, 8.583, 8.917, 9.375, 10.333, 11.208, 12.042, 12.958, 14.250, 14.542, 15.375, 15.542, 16.292, 16.458,
        16.750, 17.083, 17.250, 17.458, 18.167, 19.000, 19.208, 19.542, 19.833, 20.000, 20.250]
END = 21.083
# one take per segment: (race, take start, take end) - LAP 1 takes only, each used once
TAKES = [('sing', 0.5, 10.3),      # hook: the grid under the lights
         ('austria', 4.64, 11.6), ('baku', 5.4, 10.44), ('monza', 11.74, 20.06), ('sing', 10.32, 13.84),
         ('dutch', 6.34, 13.9),                                        # five launches
         ('baku', 10.44, 13.12), ('monaco', 7.88, 13.12), ('dutch', 23.46, 27.14), ('baku', 13.12, 15.2),
         ('baku', 20.68, 25.0), ('monaco', 13.12, 18.6), ('monza', 20.06, 25.02), ('baku', 25.0, 28.68),
         ('austria', 26.2, 29.44), ('sing', 17.64, 21.32), ('monaco', 52.48, 64.44), ('baku', 38.82, 48.94),
         ('sing', 25.2, 32.08), ('monza', 29.3, 33.42), ('austria', 11.6, 15.56), ('monaco', 40.24, 44.5),
         ('monaco', 83.36, 89.4), ('dutch', 13.9, 18.18), ('baku', 48.94, 57.56),
         ('monaco', 18.6, 25.64),                                      # the breath: LAP 1. IS WAR.
         ('austria', 15.56, 21.28), ('dutch', 18.18, 23.46), ('monza', 25.02, 29.3), ('sing', 21.32, 25.2),
         ('austria', 29.44, 36.4), ('monaco', 25.64, 32.16), ('sing', 13.84, 17.64), ('austria', 45.52, 53.72),
         ('sing', 32.08, 38.0), ('monaco', 65.96, 83.3), ('dutch', 33.5, 36.4), ('monza', 33.42, 38.78),
         ('baku', 15.2, 20.68), ('monaco', 32.16, 40.24), None, ('austria', 21.8, 26.2), ('baku', 28.68, 38.8)]
WORDS = [(0.05, 0.84, 'YOU'), (0.86, 1.31, 'READY?'), (12.958, 13.58, 'LAP 1.'), (13.6, 14.24, 'IS WAR.'),
         (20.25, 20.64, 'AUSTIN.'), (20.66, END, 'YOU READY?')]


def plan():
    segs = list(zip(CUTS, CUTS[1:] + [END]))
    evs = actionsync.events(SONG, 0, 0, END)
    out = []
    for (a, b), tk in zip(segs, TAKES):
        if tk is None:
            out.append(dict(t=a, dur=b - a, race='white', src=0.0, met=0, n=0, err=[])); continue
        race, t0, t1 = tk
        dur = b - a
        if a == 0:                                    # the hook is a held look, not an action
            out.append(dict(t=a, dur=dur, race=race, src=t0 + 2.0, met=0, n=0, err=[])); continue
        src, met, n, err = actionsync.fit(F[race], a, dur, evs, (t0 + 0.08, max(t0 + 0.1, t1 - dur - 0.08)))
        out.append(dict(t=a, dur=dur, race=race, src=src, met=met, n=n, err=err))
        print(f'{a:6.3f} {dur:5.2f}s {race:8s} @{src:7.3f}  action on sound {met}/{n} {err}')
    json.dump(out, open(os.path.join(S, 'bd_plan.json'), 'w'))
    return out


def stills(p):
    from PIL import Image
    import io
    ims = []
    for s in p:
        if s['race'] == 'white': ims.append(Image.new('RGB', (W // 4, H // 4), 'white')); continue
        r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f"{s['src'] + s['dur'] / 2:.3f}", '-i', F[s['race']], '-frames:v', '1',
                            '-vf', f'crop={W}:{H}:{X0}:{Y0},scale={W // 4}:-2', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True)
        ims.append(Image.open(io.BytesIO(r.stdout)).convert('RGB'))
    cols = 8; rows = (len(ims) + cols - 1) // cols; w, h = ims[0].size
    B = Image.new('RGB', (cols * w, rows * h))
    for i, im in enumerate(ims): B.paste(im, ((i % cols) * w, (i // cols) * h))
    out = os.path.join(S, 'qc', 'bd_stills.jpg'); B.save(out, quality=85); print(out)


def render(p, out):
    tmp = os.path.join(S, 'tmp_bd'); os.makedirs(tmp, exist_ok=True)
    fr = [round(s['t'] * FPS) for s in p] + [round(END * FPS)]
    parts = []
    for i, s in enumerate(p):
        n = fr[i + 1] - fr[i]; part = os.path.join(tmp, f's{i:02d}.mp4'); parts.append(part)
        if s['race'] == 'white':
            cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'color=white:s={W}x{H}:r={FPS}', '-frames:v', str(n)]
        else:
            cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', f"{s['src']:.3f}", '-i', F[s['race']], '-frames:v', str(n), '-an',
                   '-vf', f'fps={FPS},crop={W}:{H}:{X0}:{Y0},{GRADE},setsar=1']
        subprocess.run(cmd + ['-c:v', 'libx264', '-crf', '10', '-preset', 'fast', '-pix_fmt', 'yuv420p', part], check=True)
    lst = os.path.join(tmp, 'list.txt'); open(lst, 'w').write(''.join(f"file '{x}'\n" for x in parts))
    vid = os.path.join(tmp, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid], check=True)
    pngs = [wmtext.word_png(w, W, H, os.path.join(tmp, f'w{i}.png')) for i, (_, _, w) in enumerate(WORDS)]
    chain, last = wmtext.overlay_filter(WORDS, 2, '[0:v]')
    fc = chain + f"[1:a]atrim=0:{END:.3f},afade=t=out:st={END - 0.35:.3f}:d=0.35[a]"
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', vid, '-i', SONG]
    for pth in pngs: cmd += ['-loop', '1', '-i', pth]
    subprocess.run(cmd + ['-filter_complex', fc, '-map', last, '-map', '[a]', '-t', f'{END:.3f}', '-r', str(FPS),
                          '-c:v', 'libx264', '-crf', '10', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', out], check=True)
    print(out)


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'render'
    actionsync.FPS = FPS
    pj = os.path.join(S, 'bd_plan.json')
    if mode == 'fit': plan()
    elif mode == 'stills': stills(json.load(open(pj)))
    else: render(json.load(open(pj)), os.path.join(S, 'out', f'bd_lap1_ready_{FPS}.mp4'))
