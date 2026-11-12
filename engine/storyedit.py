"""Story edit (Desmond, Nov 12 - EDITING_RULES "STORY FIRST", refs AD1-AD3): ONE continuous commentary run with its own
pictures (never chopped), the song under all of it, captions from the commentator's words, then an ENDING montage
(black-and-white hero shots, the song up full) - in a square 1:1 picture centred in a 1080x1920 frame.
render(cfg, scratch, out) - cfg keys:
  name, fps, files {key: path}
  voice   [(key, a, b)]                the story parts, each one continuous run - sound AND picture of files[key] from a to b,
                                       played straight (a part starts and ends on a finished sentence; parts = setup, the
                                       moment, the payoff - never two pieces of the same moment)
  words   [(part, t, 'TEXT')]          caption lines on the source clock of that part ('TEXT' shows from t until the next)
  ending  [(key, src_in, dur)]         ending montage shots (black-and-white, high contrast)
  endcap  'TEXT'                       big caption over the ending (e.g. 'P21 > P2.')
  song    path, song_in (s into the song where the edit starts), song_under (level under the voice, default 0.22)
  title   'LINE 1|LINE 2'              small title in the black bar above the picture
  crop    'x' offset of the 1080x1080 crop in the 1920x1080 source (default centre 420), grade (look.GRADES key)"""
import os, subprocess
import look

W = 1080


def run(cmd):
    subprocess.run(cmd, check=True, stdin=subprocess.DEVNULL)


def render(cfg, scratch, out):
    fps, F = cfg.get('fps', 50), cfg['files']
    tmp = os.path.join(scratch, 'tmp_' + cfg['name']); os.makedirs(tmp, exist_ok=True)
    sq = f"crop=1080:1080:{cfg.get('crop', 420)}:0,{look.GRADES[cfg.get('grade', 'bright')]}"
    spans, off = [], 0.0
    for k, a, b in cfg['voice']: spans.append((off, k, a, b)); off += b - a
    body_d = off
    # 1. the body: each part rendered straight (picture + voice), then joined
    bparts = []
    for i, (_, k, a, b) in enumerate(spans):
        p = os.path.join(tmp, f'part{i}.mov'); bparts.append(p)
        run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.3f}', '-t', f'{b - a:.3f}', '-i', F[k], '-vf', f'fps={fps},{sq},setsar=1',
             '-af', 'aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:d=0.04,afade=t=out:st=%.3f:d=0.08' % (b - a - 0.08),
             '-r', str(fps), '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', p])
    lst = os.path.join(tmp, 'body.txt'); open(lst, 'w').write(''.join(f"file '{p}'\n" for p in bparts))
    body = os.path.join(tmp, 'body.mov')
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', body])
    # 2. the ending: black-and-white hero montage
    parts = []
    for i, (ek, si, d) in enumerate(cfg['ending']):
        p = os.path.join(tmp, f'end{i:02d}.mp4'); parts.append(p)
        run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{si:.3f}', '-t', f'{d:.3f}', '-i', F[ek], '-an', '-vf',
             f"fps={fps},crop=1080:1080:{cfg.get('crop', 420)}:0,hue=s=0,eq=contrast=1.55:brightness=0.03,{look.SHARPEN},setsar=1",
             '-r', str(fps), '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-pix_fmt', 'yuv420p', p])
    lst = os.path.join(tmp, 'end.txt'); open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    ending = os.path.join(tmp, 'ending.mp4')
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', ending])
    end_d = sum(d for _, _, d in cfg['ending']); total = body_d + end_d
    # 3. captions (commentator's words, solid style) + the ending caption
    texts, ws = [], cfg.get('words', [])
    et = lambda part, t: spans[part][0] + t - spans[part][2]
    for i, (part, t, txt) in enumerate(ws):
        end = spans[part][0] + spans[part][3] - spans[part][2]
        t1 = min(et(*ws[i + 1][:2]), end) if i + 1 < len(ws) and ws[i + 1][0] == part else end
        texts.append((et(part, t), min(t1, et(part, t) + 2.2) - 0.02, txt, 64, 0.82))
    if cfg.get('endcap'): texts.append((body_d + 0.4, total - 0.3, cfg['endcap'], 150, 0.5))
    pngs = []
    for i, (_, _, txt, size, cy) in enumerate(texts):
        pngs.append(look.caption_png(txt, W, W, os.path.join(tmp, f'c{i:03d}.png'), size, cy))
    # 4. assemble: body + ending, captions, square -> 1080x1920 with title, voice + song
    # ONE caption track (an image sequence with durations) - 124 looped PNG inputs took 6 GB of RAM and the PC's
    # out-of-memory killer took ffmpeg and the Claude app down with it (Nov 12, 06:13).
    blank = os.path.join(tmp, 'blank.png')
    from PIL import Image
    Image.new('RGBA', (W, W), (0, 0, 0, 0)).save(blank)
    seq, t = [], 0.0
    for p, (t0, t1, *_) in sorted(zip(pngs, texts), key=lambda x: x[1][0]):
        if t0 > t + 0.001: seq.append((blank, t0 - t))
        seq.append((p, t1 - max(t0, t))); t = t1
    seq.append((blank, max(0.1, total - t))); seq.append((blank, 0.04))
    capl = os.path.join(tmp, 'caps.txt')
    open(capl, 'w').write(''.join(f"file '{p}'\nduration {d:.3f}\n" for p, d in seq if d > 0))
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', body, '-i', ending, '-ss', f"{cfg.get('song_in', 0):.3f}", '-i', cfg['song'],
           '-f', 'concat', '-safe', '0', '-i', capl]
    chain = f'[0:v][1:v]concat=n=2:v=1:a=0[cat];[3:v]fps={fps},format=rgba[caps];[cat][caps]overlay=0:0:eof_action=pass[capd];'
    cur = '[capd]'
    # branding INSIDE the picture: sliding white title banner, then the see-through DEX EDITS mark (Desmond, Nov 12)
    cmd += ['-loop', '1', '-framerate', str(fps), '-t', f'{total:.3f}', '-i', look.banner_png(cfg.get('title', 'DEX EDITS'), os.path.join(tmp, 'banner.png'))]
    chain += f"{cur}{look.SHARPEN if cfg.get('grade') else 'null'},pad=1080:1920:0:420:black[pd];"
    flt, cur = look.brand_filter('[pd]', 4, total)
    chain += flt + f"{cur}fade=t=in:d=0.15,fade=t=out:st={total - 1.2:.3f}:d=1.2[vout];"
    under = cfg.get('song_under', 0.22)
    chain += (f"[0:a]aformat=channel_layouts=stereo,volume={cfg.get('voice_gain', 1.6)},apad=whole_dur={total:.3f}[vo];"
              f"[2:a]aformat=channel_layouts=stereo,atrim=0:{total:.3f},asetpts=PTS-STARTPTS,"
              f"volume='if(lt(t,{body_d - 0.3:.3f}),{under},{under}+(1-{under})*min(1,(t-{body_d - 0.3:.3f})/0.6))':eval=frame,"
              f"afade=t=out:st={total - 2.5:.3f}:d=2.5[so];[vo][so]amix=inputs=2:normalize=0,alimiter=limit=0.9[aout]")
    run(cmd + ['-filter_complex', chain, '-map', '[vout]', '-map', '[aout]', '-t', f'{total:.3f}', '-r', str(fps)]
        + look.encode_args(total, min(14, 92 * 8 / total)) + ['-c:a', 'aac', '-b:a', '256k', out])
    return out, body_d, total
