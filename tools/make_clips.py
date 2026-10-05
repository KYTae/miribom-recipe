"""hero clips for recipes 01-13, 20 (muted loops + poster jpg)."""
import subprocess, os
R='/home/claude/reel/'; O='/mnt/attach/outputs/'
OUT='/home/claude/site/assets/clips/'
W=(640,360); T=(540,675)
J=[ # name, src, start, dur, crop(w:h:x:y or None), size
 ('01-hero', O+'miribom_reels_02_led_jack_v2.mp4', 15.5, 5, '1080:607:0:600', W),
 ('03-hero', R+'lisa/mg_04_inline_aviator.mp4', 0.0, 4.5, '1920:1080:0:296', W),
 ('04-hero', O+'miribom_reels_04_system_prompt.mp4', 24.6, 5, '1080:607:0:600', W),
 ('05-hero', O+'miribom_reels_05_secret_codes.mp4', 2.0, 5, '1000:1250:40:300', T),
 ('06-hero', R+'dj/src.mp4', 40.0, 5, None, W),
 ('07-hero', R+'lens/src.mp4', 1.5, 5, None, W),
 ('08-hero', R+'fly/robot.mp4', 2.0, 5, '720:900:0:240', T),
 ('09-hero', O+'miribom_reels_09_ai_saju.mp4', 21.0, 5, '1080:607:0:600', W),
 ('10-hero', R+'motion/ajith.mp4', 11.0, 5, None, W),
 ('11-hero', R+'cmp/zentrix.mp4', 11.5, 5, '720:900:0:280', T),
 ('12-hero', R+'app/jaimin.mp4', 4.0, 5, '2880:1620:0:270', W),
 ('20-hero', R+'r20/miribom_reels_20_office_ai.mp4', 1.0, 5, '936:1170:72:476', T),
]
for name, src, ss, d, crop, (w, h) in J:
    vf = (f'crop={crop},' if crop else '') + f'scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps=30'
    subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(ss),'-t',str(d),'-i',src,'-an','-vf',vf,'-c:v','libx264','-crf','26','-preset','slow','-pix_fmt','yuv420p','-movflags','+faststart',OUT+name+'.mp4'],check=True)
    subprocess.run(['ffmpeg','-loglevel','error','-y','-ss','2.2','-i',OUT+name+'.mp4','-frames:v','1','-q:v','4',OUT+name+'.jpg'],check=True)
    print(name, os.path.getsize(OUT+name+'.mp4')//1024, 'KB')

# 13: neutral side-by-side (left Claude half, right GPT half)
src=R+'vs/vs_shneural.mp4'
subprocess.run(['ffmpeg','-loglevel','error','-y','-ss','6','-t','5','-i',src,'-ss','22','-t','5','-i',src,'-an','-filter_complex',
 '[0:v]scale=-2:360,crop=320:360,fps=30[a];[1:v]scale=-2:360,crop=320:360,fps=30[b];[a][b]hstack,drawbox=x=319:y=0:w=2:h=360:color=white@0.9:t=fill',
 '-c:v','libx264','-crf','26','-preset','slow','-pix_fmt','yuv420p','-movflags','+faststart',OUT+'13-hero.mp4'],check=True)
subprocess.run(['ffmpeg','-loglevel','error','-y','-ss','2.2','-i',OUT+'13-hero.mp4','-frames:v','1','-q:v','4',OUT+'13-hero.jpg'],check=True)
