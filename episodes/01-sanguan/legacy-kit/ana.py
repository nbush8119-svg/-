import numpy as np,subprocess
from scipy.signal import butter,sosfilt
SR=22050
x=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i','ace3605.wav','-f','f32le','-ac','1','-ar',str(SR),'-']),np.float32).astype(float)
hop=256;n=len(x)//hop
frames=np.lib.stride_tricks.sliding_window_view(np.pad(x,(0,1024)),1024)[::hop][:n]*np.hanning(1024)
S=np.abs(np.fft.rfft(frames,axis=1));L=np.log1p(S*10)
flux=np.r_[0,np.maximum(0,np.diff(L,axis=0)).sum(1)];flux-=np.convolve(flux,np.ones(32)/32,'same');flux=np.maximum(flux,0)
fr=SR/hop
res=[]
for bpm in np.arange(119.0,121.51,0.05):
    per=60/bpm*fr
    for p in np.arange(0,per,0.5):
        idx=np.round(np.arange(p,len(flux)-1,per)).astype(int)
        res.append((flux[idx].sum(),bpm,p/fr))
res.sort(reverse=True);print('best bpm/phase',[(round(b,2),round(p,3)) for s,b,p in res[:5]])
s,bpm,ph=res[0];beat=60/bpm
# kick-band energy at each beat -> find bar phase (downbeat) and big transitions
sos=butter(4,120,'lp',fs=SR,output='sos');lo=sosfilt(sos,x)
bt=np.arange(ph,len(x)/SR-0.1,beat)
e=np.array([np.sqrt((lo[int(t*SR):int((t+0.08)*SR)]**2).mean()) for t in bt])
ed=20*np.log10(e+1e-9)
np.save('beats.npy',bt)
print('beat',beat,'n',len(bt))
for i in range(0,len(bt),4):
    print(f'beat {i:3d} t={bt[i]:6.2f}  kick-band', ' '.join(f'{v:5.1f}' for v in ed[i:i+4]))
