"""Filme une démo de site en format téléphone (défilement doux) -> .webm. Usage : filmer_demo.py page.html sortie_dossier"""
import sys, asyncio, pathlib
from playwright.async_api import async_playwright
async def main(page_html, out):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        ctx = await b.new_context(viewport={'width':390,'height':844}, device_scale_factor=2,
                                  record_video_dir=out, record_video_size={'width':390,'height':844})
        pg = await ctx.new_page()
        await pg.goto(pathlib.Path(page_html).resolve().as_uri(), wait_until='networkidle')
        await pg.evaluate("document.documentElement.style.scrollBehavior='auto'")
        await pg.wait_for_timeout(1800)
        h = await pg.evaluate('document.documentElement.scrollHeight - innerHeight')
        pas = 40; dur = 20000
        for i in range(1, dur//pas+1):
            await pg.evaluate(f'window.scrollTo(0,{h}*{i}/{dur//pas})'); await pg.wait_for_timeout(pas)
        await pg.wait_for_timeout(1500)
        await pg.evaluate('window.scrollTo({top:0,behavior:"smooth"})'); await pg.wait_for_timeout(1500)
        v = pg.video; await ctx.close(); print(await v.path()); await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2]))
# Conversion en MP4 lisible sur iPhone (ffmpeg fourni par le paquet imageio-ffmpeg) :
#   F=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
#   $F -ss 0.8 -i demo.webm -c:v libx264 -pix_fmt yuv420p -crf 23 -movflags +faststart demo.mp4
