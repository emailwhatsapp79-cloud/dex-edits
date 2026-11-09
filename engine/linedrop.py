"""The "line -> drop" edit (refs U1 Gru, BF Spider-Man, BG Antonelli): a real line from the footage (commentary, radio,
interview) builds over the quiet part of the song with its own picture in sync, its payoff word IS the drop, then a cut on
every beat (or every 2), optionally an OUTRO line at the end with the song dipped under it.
render(cfg) - cfg keys:
  name, song, drop (song second of the drop), beat (s), files {key: path}, size (W, H), fps
  talk  [(key, a, b, pic_lead[, pic_key, pic_in])]  source spans played in order, voice + picture in sync (pic_lead delays
                                 the picture); with pic_key/pic_in the voice plays OVER another shot (cold open: frame 1 = action)
  words [(key, t, 'WORD')]       spoken words (source times); '|WORD' starts a new line
  big   ('TEXT', beats)          see-through watermark word on the drop (big_size: height share, default 0.13)
  after [(beats, key, in, take_end)]
  outro (key, a, b, words[, pics]) | None  a last spoken line after the beats, song dipped to 0.3; pics [(key, in, dur)]
                                 = the shots under that voice (last one fills the rest)
  cap (size, cy)                 spoken-word text size and height (0.6 = 40 % up from the bottom)
  hits [(after_index, offset)]   that shot's own sound laid on the song at the cut (+offset)
  intro_song                     song level before the drop (0.3 = under the voice; 0 = the moment plays raw, no music)
  shake                          True: a short mild camera shake on the drop and every cut after it (ref X1/Y1)"""
import os, subprocess
import wmtext
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

GRADE = 'eq=contrast=1.06:saturation=1.10'


def glow_png(text, W, H, out, size=48, cy=0.6):
    f = None
    while True:
        f = ImageFont.truetype(wmtext.FONT, size)
        try: f.set_variation_by_axes([800, 112])
        except Exception: pass
        if f.getlength(text) <= W * 0.82 or size <= 24: break
        size -= 2
    box = f.getbbox(text); tw, th = box[2] - box[0], box[3] - box[1]
    x, y = (W - tw) // 2 - box[0], int(H * cy - th / 2) - box[1]
    txt = Image.new('L', (W, H), 0); ImageDraw.Draw(txt).text((x, y), text, font=f, fill=235)
    glow = txt.filter(ImageFilter.GaussianBlur(max(4, size // 7))).point(lambda v: min(255, v * 2) * 0.7)
    a = Image.fromarray(np.maximum(np.array(txt), np.array(glow)).astype('uint8')).point(lambda v: int(v * 0.88))
    img = Image.new('RGBA', (W, H), (255, 255, 255, 0)); img.putalpha(a); img.save(out); return out


def render(cfg, scratch, out):
    W, H = cfg['size']; FPS = cfg.get('fps', 30); F = cfg['files']; talk = cfg['talk']
    drop_e = sum(x[2] - x[1] for x in talk)
    off = cfg['drop'] - drop_e
    beat = lambda k: drop_e + k * cfg['beat']
    after = cfg['after']; outro = cfg.get('outro')
    end_beats = beat(sum(n for n, *_ in after))
    HOLD = cfg.get('hold', 1.0) if outro else 0.0          # picture + song keep going after the last word (never end ON it)
    END = end_beats + ((outro[2] - outro[1]) if outro else 0) + HOLD
    tmp = os.path.join(scratch, 'tmp_' + cfg['name']); os.makedirs(tmp, exist_ok=True)
    parts, t = [], 0.0

    def clip(k, s, d, name):
        n = round((t + d) * FPS) - round(t * FPS); p = os.path.join(tmp, name)
        crop = cfg.get('crop', '')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{s:.3f}', '-i', F[k], '-frames:v', str(n), '-an', '-vf',
                        f'fps={FPS},{crop + "," if crop else ""}scale={W}:{H},{GRADE},setsar=1', '-c:v', 'libx264', '-crf', '12',
                        '-preset', 'fast', '-pix_fmt', 'yuv420p', p], check=True)
        parts.append(p)

    spans = []                                   # (edit start, key, a, b) of every voiced span
    for i, (k, a, b, lead, *pic) in enumerate(talk):
        spans.append((t, k, a, b)); clip(pic[0] if pic else k, pic[1] if pic else a + lead, b - a, f'a{i}.mp4'); t += b - a
    for i, (n, k, s, e) in enumerate(after):
        d = beat(sum(x for x, *_ in after[:i + 1])) - t
        assert s + d <= e + 0.03, f"{cfg['name']} after #{i} runs past its take ({s + d:.2f} > {e})"
        clip(k, s, d, f'b{i:02d}.mp4'); t += d
    if outro:
        k, a, b = outro[:3]; spans.append((t, k, a, b))
        pics = outro[4] if len(outro) > 4 else [(k, a, b - a)]       # outro voice can play OVER other shots (the celebration)
        rest = b - a
        for j, (pk, ps, pd) in enumerate(pics):
            d = rest + HOLD if j == len(pics) - 1 else pd
            clip(pk, ps, d, f'z{j}.mp4'); t += d; rest -= d
    lst = os.path.join(tmp, 'list.txt'); open(lst, 'w').write(''.join(f"file '{x}'\n" for x in parts))
    vid = os.path.join(tmp, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid], check=True)

    def edit_t(k, st):
        for e0, kk, a, b in spans:
            if kk == k and a - 0.01 <= st <= b + 0.01: return e0 + st - a
        raise ValueError((k, st))

    def build(words, last_end):
        res, line = [], []
        for i, (k, st, w) in enumerate(words):
            if w.startswith('|'): line = []; w = w[1:]
            line.append(w)
            if i + 1 < len(words):
                nk, nt, nw = words[i + 1]
                end = edit_t(nk, nt) - 0.001
                if nw.startswith('|'):                 # hold a finished line at most 0.6 s
                    end = min(end, edit_t(k, st) + 0.9)
            else:
                end = last_end
            res.append((edit_t(k, st), end, ' '.join(line)))
        return res

    texts = build(cfg['words'], drop_e - 0.001)
    big, nb = cfg['big']
    texts.append((drop_e, beat(nb) - 0.02, big))
    if outro: texts += build(outro[3], END - HOLD + 0.4)
    size, cy = cfg.get('cap', (48, 0.6))
    pngs = []
    for i, (_, _, w) in enumerate(texts):
        p = os.path.join(tmp, f'c{i:02d}.png')
        pngs.append(wmtext.word_png(w, W, H, p, size=int(H * cfg.get('big_size', 0.13))) if w == big else glow_png(w, W, H, p, size, cy))
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', vid, '-ss', f'{max(0.0, off):.3f}', '-i', cfg['song']]
    for p in pngs: cmd += ['-loop', '1', '-framerate', str(FPS), '-t', f'{END:.3f}', '-i', p]
    src = '[0:v]'
    if cfg.get('shake'):
        hits = [drop_e] + [beat(sum(x for x, *_ in after[:i + 1])) for i in range(len(after) - 1)]
        sh = lambda amp, f, ph: '+'.join(f"between(t,{h:.3f},{h + 0.28:.3f})*{amp}*sin(2*PI*{f}*(t-{h:.3f})+{ph})*(1-(t-{h:.3f})/0.28)" for h in hits)
        cw, ch = int(W * 0.94) // 2 * 2, int(H * 0.94) // 2 * 2; mx, my = (W - cw) // 2, (H - ch) // 2
        a = max(6, W // 60)
        src = f"[0:v]crop={cw}:{ch}:'{mx}+{sh(a, 18, 0)}':'{my}+{sh(a * 0.65, 23, 1.3)}',scale={W}:{H}:flags=lanczos,setsar=1[sh];"
    chain, last = wmtext.overlay_filter(texts, 2, '[sh]' if cfg.get('shake') else '[0:v]')
    if cfg.get('shake'): chain = src + chain
    n0 = 2 + len(pngs); fx, labels = '', []
    for i, (e0, k, a, b) in enumerate(spans):        # the voices, in sync; the last talk span runs on through the drop word
        tail = 0.55 if i == len(talk) - 1 else (0.35 if i >= len(talk) else 0.2)   # a breath after every span: no clipped last word
        cmd += ['-ss', f'{a:.3f}', '-t', f'{b - a + tail:.3f}', '-i', F[k]]
        fx += (f"[{n0 + i}:a]aformat=channel_layouts=stereo,highpass=f=90,afade=t=in:d=0.03,afade=t=out:st={b - a + tail - 0.12:.3f}:d=0.12,"
               f"volume={cfg.get('voice', 1.8)},adelay={int(e0 * 1000)}|{int(e0 * 1000)}[v{i}];")
        labels.append(f'[v{i}]')
    n1 = n0 + len(spans)
    for j, (idx, o) in enumerate(cfg.get('hits', [])):
        _, k, s, _ = after[idx]; at = beat(sum(x for x, *_ in after[:idx])) + o
        cmd += ['-ss', f'{s + o:.3f}', '-t', '0.6', '-i', F[k]]
        fx += (f"[{n1 + j}:a]aformat=channel_layouts=stereo,afade=t=out:st=0.3:d=0.3,volume=1.5,adelay={int(at * 1000)}|{int(at * 1000)}[x{j}];")
        labels.append(f'[x{j}]')
    o_start = end_beats if outro else END + 1
    pre = f"adelay={int(-off * 1000)}|{int(-off * 1000)}," if off < 0 else ''   # song starts AT the drop (its bar 1 = the drop)
    fx += (f"[1:a]{pre}atrim=0:{END:.3f},asetpts=PTS-STARTPTS,volume='if(lt(t,{drop_e - 0.04:.3f}),{cfg.get("intro_song", 0.3)},if(gt(t,{END - HOLD + 0.3:.3f}),0.8,if(gt(t,{o_start:.3f}),0.3,1.0)))':eval=frame,"
           f"afade=t=out:st={END - cfg.get('fade', 0.4):.3f}:d={cfg.get('fade', 0.4)}[song];[song]{''.join(labels)}amix=inputs={len(labels) + 1}:normalize=0,alimiter=limit=0.85[a]")
    subprocess.run(cmd + ['-filter_complex', chain + fx, '-map', last, '-map', '[a]', '-t', f'{END:.3f}', '-r', str(FPS),
                          '-c:v', 'libx264', '-crf', '12', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', out], check=True)
    return out, drop_e, END
