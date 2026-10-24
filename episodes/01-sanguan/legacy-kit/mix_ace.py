import numpy as np,subprocess,wave,re,json
SR=48000;DUR=74.5;N=int(SR*DUR)
def rd(p,ch=2):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',p,'-f','f32le','-ac',str(ch),'-ar',str(SR),'-']),np.float32).astype(float).reshape(-1,ch)[:N]
def wr(p,y):
    w=wave.open(p,'wb');w.setnchannels(y.shape[1]);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(y,-1,1)*32767).astype('<i2').tobytes())
m=rd('music_ace_edit.wav');m=np.pad(m,((0,N-len(m)),(0,0)))
v=rd('vo_proc.wav')[:,0];v=np.pad(v,(0,N-len(v)))
s=open('index.html').read();cues=eval(re.search(r'const CUES=(\[[\s\S]*?\]);',s).group(1))
db=lambda a:20*np.log10(np.sqrt((a**2).mean())+1e-12)
# voice-driven ducking envelope (smooth): 1 where silent, depth where speaking
env=np.sqrt(np.convolve(v**2,np.ones(int(0.05*SR))/int(0.05*SR),'same'))
speak=(env>10**(-38/20)).astype(float)
# attack 40ms / release 350ms smoothing
g=np.empty(N);a_up=1-np.exp(-1/(0.35*SR));a_dn=1-np.exp(-1/(0.04*SR));acc=0.0
for i in range(N):
    tgt=speak[i];acc+= (a_dn if tgt>acc else a_up)*(tgt-acc);g[i]=acc
t=np.arange(N)/SR
target=10.0
gain_db=np.zeros(N)   # per-cue level, applied only while speaking via g
for c0,c1,_ in cues:
    i0,i1=int(c0*SR),int(c1*SR);vm=v[i0:i1];mm=m[i0:i1].mean(1)
    sp=speak[i0:i1]>0.5
    need=(db(vm[sp])-target)-db(mm[sp]) if sp.any() else 0
    gain_db[i0:i1]=min(0,need)
# smooth cue gains, then duck = interp between gap level and cue level by g
gs=np.convolve(gain_db,np.ones(int(0.3*SR))/int(0.3*SR),'same')
GAP=-2.0   # gaps: slightly under full
total_db=GAP*(1-g)+gs*g + 0
# intro before first word & end card: full-ish
total_db=np.where(t>71.3,np.maximum(total_db,-1.0),total_db)
mg=m*(10**(total_db/20))[:,None]
wr('music_ace_ducked.wav',mg)
for c0,c1,txt in cues:
    i0,i1=int(c0*SR),int(c1*SR);sp=speak[i0:i1]>0.5
    print(f'{c0:6.2f} diff {db(v[i0:i1][sp])-db(mg[i0:i1].mean(1)[sp]):5.1f}  {txt[:12]}')
