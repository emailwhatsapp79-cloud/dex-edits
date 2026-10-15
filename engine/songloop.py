"""Make a longer sound from a short TikTok sound: song[0:a] + song[b:c] joined on two matching hits (a and b),
with a gentle fade-out at the end - so the edit can run 20-25 s and END on a phrase instead of stopping."""
import subprocess, sys


def loop(src, out, a, b, c, fade=1.0, xf=0.03):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-i', src, '-filter_complex',
                    f"[0]atrim=0:{a + xf / 2:.3f},asetpts=PTS-STARTPTS[p];"
                    f"[1]atrim={b - xf / 2:.3f}:{c:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={c - b - fade:.3f}:d={fade}[q];"
                    f"[p][q]acrossfade=d={xf}:c1=tri:c2=tri", '-ac', '2', '-ar', '44100', '-c:a', 'libmp3lame', '-b:a', '256k', out],
                   check=True)
    return out


if __name__ == '__main__':
    print(loop(sys.argv[1], sys.argv[2], *map(float, sys.argv[3:6])))
