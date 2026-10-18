"""BB - '911, what's your emergency?' (Desmond's idea, Oct 18): Porsche 911 pun. A phone rings, the operator answers,
the caller says "I'd like to report a 911" -> Montagem Kali (#5) drops into a night 911 montage -> the operator:
"Sir, a 911 is not an emergency." over Porsche's own "THERE IS NO SUBSTITUTE" end shot.
Voices are our own TTS (never a real emergency recording). Footage: Porsche newsroom film p_328485 (1080p, native size,
HORIZONTAL - no crop, no scale). Cuts every 2 beats of the song from the drop."""
import os, subprocess, sys

S = os.environ.get('SCRATCH', '/tmp')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.environ.get('DEX_ASSETS', os.path.join(os.path.dirname(ROOT), 'dex-edits-assets'))
SRC = os.path.join(S, 'src_pcar', 'p_328485.mp4')
VO = os.path.join(S, 's911')                     # op_en-US-AriaNeural_t.wav, caller_guy_t.wav, op2_jenny_t.wav
SONG = os.path.join(ASSETS, 'songs', '05_montagem_kali_slowed.m4a')
FONT = os.path.join(ROOT, 'fonts', 'Anton.ttf')
SONG_AT_0, DROP, END = 12.60, 7.20, 21.70        # song 19.80 (the re-entry after the break) lands on the drop
SHOTS = [(0.00, 76.40), (2.60, 80.84), (4.40, 100.60),                       # the call: headlights in the dark
         (7.20, 8.88), (8.08, 104.90), (9.11, 85.70), (10.13, 7.95), (11.01, 109.46), (11.89, 89.05),
         (12.77, 9.85), (13.80, 83.86), (14.82, 64.75), (15.70, 57.65), (16.58, 66.10),
         (17.47, 114.00)]                                                   # end: 'THERE IS NO SUBSTITUTE'
VOICES = [('op_ava_t.wav', 1.60, True), ('caller_andrew_t.wav', 4.35, False), ('op2_ava_t.wav', 17.70, True)]   # smoother voices (Desmond)
TEXT = [(0.15, 1.45, 'CALLING 911...', 64, 0.46), (1.60, 4.15, "911, WHAT'S YOUR EMERGENCY?", 58, 0.80),
        (4.35, 7.15, "YEAH... I'D LIKE TO REPORT A 911.", 58, 0.80), (7.20, 8.08, '911.', 300, 0.33),
        (17.70, 20.20, 'SIR, A 911 IS NOT AN EMERGENCY.', 58, 0.80)]


def dt(t0, t1, text, fs, y):
    text = text.replace("'", '’').replace(':', '\\:').replace(',', '\\,')
    return (f",drawtext=fontfile={FONT}:text='{text}':fontsize={fs}:fontcolor=white:borderw=3:bordercolor=black@0.5:"
            f"shadowcolor=black@0.6:shadowy=4:x=(w-text_w)/2:y=h*{y}:enable='between(t,{t0},{t1})'")


def main():
    os.makedirs(os.path.join(S, 'out'), exist_ok=True)
    ts = [t for t, _ in SHOTS] + [END]
    fr = [round(t * 30) for t in ts]
    inp, fc, cat = [], '', ''
    for i, ((t, a), n) in enumerate(zip(SHOTS, [b - a for a, b in zip(fr, fr[1:])])):
        inp += ['-ss', f'{a}', '-i', SRC]
        fc += f'[{i}:v]fps=30,trim=end_frame={n},setpts=PTS-STARTPTS,setsar=1,eq=contrast=1.06:saturation=1.05[v{i}];'
        cat += f'[v{i}]'
    k = len(SHOTS)
    fc += f'{cat}concat=n={k}:v=1:a=0[vc];[vc]null' + ''.join(dt(*x) for x in TEXT) + '[v];'
    phone = 'highpass=f=260,lowpass=f=3800,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,volume=1.9'   # soft line, no harsh edge
    fc += (f"aevalsrc='0.22*(sin(2*PI*440*t)+sin(2*PI*480*t))':d=1.2:s=48000,{phone},adelay=150|150[ring];"
           f"anoisesrc=d=0.04:a=0.35:r=48000,lowpass=f=2500,adelay=1450|1450[click];"
           f"anoisesrc=d=5.75:c=pink:a=0.012:r=48000,{phone},afade=t=in:d=0.2,afade=t=out:st=5.4:d=0.35,adelay=1450|1450[line];")   # faint line hiss under the call
    mix = '[ring][click][line]'
    for j, (f, at, tel) in enumerate(VOICES):
        inp += ['-i', os.path.join(VO, f)]
        fc += f"[{k + j}:a]aresample=48000,{phone if tel else 'highpass=f=90,acompressor=threshold=-20dB:ratio=2,volume=3.2,aecho=0.8:0.5:18:0.12'},adelay={int(at * 1000)}|{int(at * 1000)}[vo{j}];"
        mix += f'[vo{j}]'
    inp += ['-ss', f'{SONG_AT_0}', '-i', SONG]
    s = k + len(VOICES)
    fc += (f"[{s}:a]atrim=0:{END},asetpts=PTS-STARTPTS,aresample=48000,"
           f"volume='if(lt(t,{DROP}),0.10,if(between(t,17.6,20.3),0.35,1))':eval=frame,afade=t=out:st={END - 0.8}:d=0.8[song];"
           f"{mix}[song]amix=inputs={len(VOICES) + 4}:duration=longest:normalize=0,alimiter=limit=0.95,atrim=0:{END}[a]")
    out = os.path.join(S, 'out', 'bb_911_emergency.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-t', f'{END}',
                    '-c:v', 'libx264', '-crf', '10', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', out], check=True)
    sys.path.insert(0, os.path.dirname(__file__)); import brand
    print(brand.brand(out, out.replace('.mp4', '_DEX.mp4')))


if __name__ == '__main__':
    main()
