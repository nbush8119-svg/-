import numpy as np,subprocess,wave
SR=48000;DUR=74.5;N=int(SR*DUR)
x=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i','ace3605.wav','-f','f32le','-ac','2','-ar',str(SR),'-']),np.float32).reshape(-1,2).astype(float)
BEAT=60/121;PH=0.319
T=lambda b:PH+b*BEAT
d1=4.61-T(8); d2=d1+16*BEAT; d3=(T(116)+d2)-T(136)
# (track_start, track_end, video_offset)
segs=[(0.0,T(88),d1),(T(72),T(88),d1+16*BEAT),(T(88),T(116),d2),(T(136),len(x)/SR,d3)]
print('d1 %.3f d2 %.3f d3 %.3f  drop->video %.3f'%(d1,d2,d3,T(96)+d2))
out=np.zeros((N,2));XF=int(0.03*SR)
for k,(a,b,d) in enumerate(segs):
    i0=int(round((a-0.015)*SR)) if k else 0; i1=int(round((b-0.015)*SR))+(XF if k<len(segs)-1 else 0)
    seg=x[max(0,i0):i1].copy()
    if k: seg[:XF]*=np.sin(np.linspace(0,np.pi/2,XF))[:,None]**2
    if k<len(segs)-1: seg[-XF:]*=np.cos(np.linspace(0,np.pi/2,XF))[:,None]**2; seg=np.concatenate([seg,np.zeros((XF,2))]) if False else seg
    v0=int(round((max(0,a-0.015 if k else 0)+d)*SR))
    if k: 
        # extend previous segment tail under crossfade: append next XF of source to previous handled by overlap of fades
        pass
    j=min(N,v0+len(seg))
    if v0<N: out[max(0,v0):j]+=seg[max(0,-v0):j-v0]
t=np.arange(N)/SR
out*=np.minimum(1,(DUR-t)/1.8)[:,None]
w=wave.open('music_ace_edit.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(out,-1,1)*32767).astype('<i2').tobytes())
# report joints
for k,(a,b,d) in enumerate(segs): print(f'seg{k}: track {a:6.2f}-{b:6.2f} -> video {a+d:6.2f}-{b+d:6.2f}')
