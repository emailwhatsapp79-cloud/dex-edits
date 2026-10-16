"""Effective resolution: for a frame, the smallest height H such that downscale->upscale loses almost nothing (PSNR>=38)."""
import cv2, numpy as np, sys, json
def eff(f):
    g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY).astype(np.float32); g=g[200:1720]  # skip watermark/bands
    h,w=g.shape
    for H in [360,480,540,720,900,1080]:
        s=H/1920; d=cv2.resize(g,(max(8,int(w*s)),max(8,int(h*s))),interpolation=cv2.INTER_AREA)
        u=cv2.resize(d,(w,h),interpolation=cv2.INTER_CUBIC)
        mse=((u-g)**2).mean(); p=99 if mse==0 else 10*np.log10(255**2/mse)
        if p>=38: return H
    return 1920
for p in sys.argv[1:]:
    c=cv2.VideoCapture(p); fps=c.get(5); n=int(c.get(7)); res=[]
    for i in range(0,n,int(fps*0.5)):
        c.set(1,i); ok,f=c.read()
        if not ok: break
        res.append(eff(f))
    r=np.array(res); print(json.dumps({'file':p.split('/')[-1],'median':int(np.median(r)),'pct_le540':round(float((r<=540).mean())*100),'pct_le360':round(float((r<=360).mean())*100),'series':res}))
