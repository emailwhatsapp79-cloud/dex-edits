"""CV - DTM: THE TITLE DECIDER, HOCKENHEIM 2026 (Mon 16 Nov 18:00, replaces Max four). Maro Engel has to win the race;
Thomas Preining only needs a top 10. Engel goes three abreast at turn eight and takes the lead, Preining follows him
through, and Engel's win is not enough: third place makes Preining a two-time DTM champion.
  1 "Still though, a top 10 finish, even if Maro Engel won the race, would be enough for Thomas Preining."
  2 "Maro Engel going full beans for the race win. Down the inside he went at turn eight. Alongside Bastian Buus,
     three abreast, because Thomas Preining got involved as well."
  3 "Engel sending it in the Mercedes and getting through, and Thomas Preining following suit."
  4 "But third place, and the champion of 2026, Tommy Preining. Tommy Preining, you are a two-time DTM champion."
  outro: a new clip on every beat (the start, the dust, wheel to wheel, the donuts in slow motion), end card.
Song: Bow Bow Bow (Zeddy Will) from 54.45 s - the loud run at 79 s lands on the outro. 25 fps, no grade.
Whisper hears 'Prining' / 'Marouengault' / 'Bastion Bouss' - captions use the real names.
Source: DTM 'The Championship Decider | DTM Hockenheimring Race 2 Highlights | Season Finale | DTM 2026' (NifV8pPz8Ec).
Usage: SRC=<sources folder> SCRATCH=<dir> python3 edit_cv_dtm_decider.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'d': (src('NifV8pPz8Ec'), 'crop=1080:1080:420:0')}
W1 = [(49.74, 'STILL THOUGH, A TOP 10 FINISH,'), (51.62, 'EVEN IF MARO ENGEL WON THE RACE,'), (53.08, 'WOULD BE ENOUGH'),
      (53.68, 'FOR THOMAS PREINING.')]
W2 = [(109.6, 'MARO ENGEL GOING FULL BEANS'), (111.62, 'FOR THE RACE WIN.'), (112.72, 'DOWN THE INSIDE HE WENT'),
      (114.28, 'AT TURN EIGHT.'), (114.96, 'ALONGSIDE BASTIAN BUUS,'), (116.22, 'THREE ABREAST,'),
      (116.8, 'BECAUSE THOMAS PREINING'), (117.36, 'GOT INVOLVED AS WELL.')]
W3 = [(122.48, 'ENGEL SENDING IT IN THE MERCEDES'), (123.7, 'AND GETTING THROUGH,'), (124.92, 'AND THOMAS PREINING'),
      (125.64, 'FOLLOWING SUIT.')]
W4 = [(233.72, 'BUT THIRD PLACE,'), (234.68, 'AND THE CHAMPION OF 2026,'), (236.7, 'TOMMY PREINING.'),
      (237.44, 'TOMMY PREINING, YOU ARE A'), (238.58, 'TWO-TIME DTM CHAMPION.')]
OUTRO = [('d', 0.5), ('d', 36.0), ('d', 80.0), ('d', 88.0), ('d', 128.0), ('d', 244.0), ('d', 241.5, 0.6)]
CFG = dict(name='dtm_decider', files=FILES,
           song=os.path.join(ASSETS, 'songs', 'trend', 'bow_bow_bow_zeddy_will.mp3'), song_in=54.45,
           title='DTM|THE DECIDER', banner_in=0.4,
           segments=[dict(type='voice', k='d', a=49.7, b=54.45, words=W1),
                     dict(type='voice', k='d', a=109.55, b=118.6, words=W2),
                     dict(type='voice', k='d', a=122.4, b=126.5, words=W3),
                     dict(type='voice', k='d', a=233.65, b=240.35, words=W4),
                     dict(type='outro', shots=OUTRO)])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'cv_dtm_decider_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
