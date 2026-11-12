"""Beat edit (Desmond, Nov 12 - ref AE1 @aelclerc "podium from the back of the grid?", 115k views): a short hype edit where
every cut lands on a hit of the song - zoom punch + shake on each cut, a white flash on the big hits - square picture in a
1080x1920 frame. Each shot is rendered on its own (low memory: safe next to the Claude app on 8 GB).
render(cfg, scratch, out) - cfg keys:
  name, fps, files {key: path}, song, song_in (song second at edit 0), cuts [song seconds of the hits], end (song second)
  build   (key, src_in)        the shot before the first cut (song_in -> cuts[0]), plain, fades in from black
  shots   [(key, src_in)]      one per gap between cuts; the last one runs from cuts[-1] to end
  flash   [shot index]         shots that open with a white flash (the drop, the big hits)
  grade   look.GRADES key or None (None = the footage as it is, Desmond's Nov 12 test)
  title, endcap                as storyedit"""
import os, subprocess
import look

W = 1080


def run(cmd):
    subprocess.run(cmd, check=True, stdin=subprocess.DEVNULL)


def render(cfg, scratch, out):
    fps, F = cfg.get('fps', 50), cfg['files']
    tmp = os.path.join(scratch, 'tmp_' + cfg['name']); os.makedirs(tmp, exist_ok=True)
    g = cfg.get('grade')
    base = f"fps={fps},crop=1080:1080:{cfg.get('crop', 420)}:0" + (f',{look.GRADES[g]}' if g else '')
    cuts, s0, end = cfg['cuts'], cfg['song_in'], cfg['end']
    spans = [(cfg['build'], s0, cuts[0], 'build')] + [
        (sh, cuts[i], cuts[i + 1] if i + 1 < len(cuts) else end, i) for i, sh in enumerate(cfg['shots'])]
    parts = []
    for j, ((k, si), a, b, i) in enumerate(spans):
        d = b - a; n = round((b - s0) * fps) - round((a - s0) * fps)
        vf = base
        if i == 'build':
            vf += f',fade=t=in:st=0:d=0.4'
        else:
            # zoom punch 1.10 -> 1.0 over 0.25 s + a decaying shake on every other cut, then the flash
            amp = 14 if i % 2 == 0 else 0
            vf += (f",zoompan=z='max(1,1.10-0.40*on/{fps})':d=1:s=1080x1080:fps={fps}"
                   f":x='iw/2-iw/zoom/2+{amp}*sin(on*1.9)*max(0,1-on/({0.3 * fps}))'"
                   f":y='ih/2-ih/zoom/2+{amp * 0.7}*sin(on*2.3+1)*max(0,1-on/({0.3 * fps}))'")
            if i in cfg.get('flash', []): vf += ',fade=t=in:st=0:d=0.08:color=white'
        p = os.path.join(tmp, f's{j:02d}.mp4'); parts.append(p)
        run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{si:.3f}', '-i', F[k], '-frames:v', str(n), '-an', '-vf', vf + ',setsar=1',
             '-r', str(fps), '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-pix_fmt', 'yuv420p', p])
    lst = os.path.join(tmp, 'list.txt'); open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    vid = os.path.join(tmp, 'video.mp4')
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid])
    total = end - s0
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', vid, '-ss', f'{s0:.3f}', '-t', f'{total:.3f}', '-i', cfg['song']]
    chain, cur = '', '[0:v]'
    if cfg.get('endcap'):
        p = look.caption_png(cfg['endcap'], W, W, os.path.join(tmp, 'endcap.png'), 150, 0.5)
        cmd += ['-loop', '1', '-framerate', str(fps), '-t', f'{total:.3f}', '-i', p]
        chain += f"[0:v][2:v]overlay=0:0:enable='gte(t,{cuts[-1] - s0:.3f})'[e];"; cur = '[e]'
    font = os.path.join(os.path.dirname(look.FONT), 'Anton.ttf')
    title, lines = '', [l for l in cfg.get('title', '').split('|') if l]
    for j, line in enumerate(lines):
        line = line.replace("'", '’').replace(':', '\\:')
        title += (f",drawtext=fontfile={font}:text='{line}':fontsize=78:fontcolor=white:x=(w-text_w)/2:"
                  f"y=420-{40 + 95 * (len(lines) - 1 - j)}-text_h")
    mark = f",drawtext=fontfile={font}:text='DEX EDITS':fontsize=40:fontcolor=white@0.55:x=(w-text_w)/2:y=1530"
    chain += f"{cur}pad=1080:1920:0:420:black{title}{mark},fade=t=out:st={total - 0.8:.3f}:d=0.8[v];"
    chain += f"[1:a]afade=t=out:st={total - 1.5:.3f}:d=1.5,alimiter=limit=0.9[a]"
    run(cmd + ['-filter_complex', chain, '-map', '[v]', '-map', '[a]', '-t', f'{total:.3f}', '-r', str(fps)]
        + look.encode_args(total, 12) + ['-c:a', 'aac', '-b:a', '256k', out])
    return out, total
