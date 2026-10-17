# Fabrique la vidéo pour une voix : animation déformée dans le temps pour suivre la voix (repères par mot), musique ajustée.
import json,subprocess,os,sys
from playwright.sync_api import sync_playwright
voix=sys.argv[1];OFF=0.8;FPS=30
R=json.load(open(f'conteur/repere-{voix}.json'))
orig=[0.7,3.55,5.6,11.2,19.6,26.2,31.5]
new=[OFF+x for x in R['debuts']]
DUR=round(new[-1]+7.0,2)
pts=[(0,0)]+list(zip(new,orig))+[(DUR,38.5)]
def warp(t):
    for (a,x),(b,y) in zip(pts,pts[1:]):
        if t<=b: return x+(y-x)*(t-a)/(b-a)
    return 38.5
env=dict(os.environ,DUREE=str(DUR+0.5));subprocess.run(['python3','musique.py'],check=True,env=env)
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'conteur/voix-{voix}.wav','-i','musique.wav','-filter_complex',
 f'[0:a]adelay={int(OFF*1000)}:all=1,apad,atrim=0:{DUR},volume=1.3,asplit=2[vx][sc];'
 '[1:a]volume=-13dB[mu];[mu][sc]sidechaincompress=threshold=0.03:ratio=5:attack=25:release=400[md];'
 f'[vx][md]amix=inputs=2:normalize=0,atrim=0:{DUR},alimiter=limit=0.89,aformat=sample_rates=44100:channel_layouts=stereo[out]',
 '-map','[out]','-c:a','aac','-b:a','192k',f'son-{voix}.m4a'],check=True)
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-','-i',f'son-{voix}.m4a',
 '-af','loudnorm=I=-15:TP=-1.5:LRA=9','-c:v','libx264','-preset','slow','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',
 '-ar','44100','-c:a','aac','-b:a','192k','-shortest',f'dig16-{voix}.mp4'],stdin=subprocess.PIPE)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file://'+os.getcwd()+'/video.html',wait_until='networkidle');pg.wait_for_timeout(1500)
    for i in range(int(FPS*DUR)):
        pg.evaluate(f'seek({warp(i/FPS):.4f})');ff.stdin.write(pg.screenshot(type='jpeg',quality=93))
    b.close()
ff.stdin.close();ff.wait();print(voix,'durée',DUR)
