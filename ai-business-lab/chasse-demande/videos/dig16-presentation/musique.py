# Musique originale DIG16 : nappe douce + arpèges légers + basse, 38 s, 44,1 kHz (composée par programme, libre de droits)
import numpy as np, wave
sr=44100; dur=38.5; t=np.arange(int(sr*dur))/sr
def note(f,start,length,amp,kind='pad'):
    n=int(length*sr);tt=np.arange(n)/sr
    if kind=='pad':
        w=sum(np.sin(2*np.pi*f*k*tt+0.3*k)/(k**1.6) for k in (1,2,3))+0.5*np.sin(2*np.pi*f*1.003*tt)
        env=np.minimum(1,tt/0.9)*np.minimum(1,(length-tt)/1.2)
    elif kind=='pluck':
        w=np.sin(2*np.pi*f*tt)+0.35*np.sin(2*np.pi*2*f*tt)+0.12*np.sin(2*np.pi*3*f*tt)
        env=np.exp(-tt*3.2)*np.minimum(1,tt/0.01)
    else: # basse
        w=np.sin(2*np.pi*f*tt)+0.2*np.sin(2*np.pi*2*f*tt)
        env=np.minimum(1,tt/0.05)*np.exp(-tt*0.9)
    out=np.zeros_like(t);i=int(start*sr)
    if i>=len(out): return out
    seg=(w*env*amp)[:len(out)-i];out[i:i+len(seg)]+=seg;return out
hz=lambda m:440*2**((m-69)/12)
# progression (Do maj7, La m7, Fa maj7, Sol 6), 4 temps à 92 bpm
beat=60/92; bar=4*beat
prog=[[48,55,59,64],[45,52,55,60],[41,48,52,57],[43,50,55,59]]
mix=np.zeros_like(t);b=0;start=0.0
while start<dur-0.5:
    ch=prog[b%4]
    for m in ch: mix+=note(hz(m+12),start,bar+0.6,0.045,'pad')
    mix+=note(hz(ch[0]-12),start,bar,0.10,'bass')
    if start>=1.5:
        arp=[ch[1]+24,ch[2]+24,ch[3]+24,ch[2]+24,ch[1]+24,ch[3]+24,ch[2]+24,ch[3]+24]
        for k,m in enumerate(arp): mix+=note(hz(m),start+k*beat/2,1.4,0.032,'pluck')
    start+=bar;b+=1
# fondu de fin et de début
fade=np.minimum(1,t/1.5)*np.clip((dur-t)/3.0,0,1)
mix*=fade
# petit écho
d=int(0.27*sr);echo=np.zeros_like(mix);echo[d:]=mix[:-d]*0.28;mix+=echo
mix/=np.max(np.abs(mix))*1.12
w=wave.open('musique.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((mix*32767).astype(np.int16).tobytes());w.close()
print('musique ok',dur)
