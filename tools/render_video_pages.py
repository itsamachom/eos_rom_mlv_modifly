"""Render static video pages from the creator's catalog; no remote embeds or API keys."""
from pathlib import Path
import html
import json
import os
import re
import urllib.parse

root=Path(__file__).resolve().parents[1];docs=root/'docs'
catalog=json.loads((root/'website-content/videos.json').read_text())
playlist=urllib.parse.urlsplit(catalog['playlist_url'])
assert playlist.scheme=='https' and playlist.hostname=='www.youtube.com' and playlist.path=='/playlist'
assert re.fullmatch(r'[A-Za-z0-9_-]+',urllib.parse.parse_qs(playlist.query)['list'][0])
items=catalog['videos'];assert items and len({v['id'] for v in items})==len(items)
for v in items:
 assert re.fullmatch(r'[A-Za-z0-9_-]{11}',v['youtube_id'])
 assert (docs/v['poster']).resolve().is_relative_to(docs.resolve()) and (docs/v['poster']).is_file()
featured=next(v for v in items if v['id']==catalog['featured'])
esc=html.escape
url=lambda v:'https://www.youtube.com/watch?v='+v['youtube_id']
css=re.search(r'site.css\?v=([^"\s]+)',(docs/'index.html').read_text()).group(1)
profiles=[('YouTube · Online2easy','https://www.youtube.com/@Online2easy'),('Facebook · Online2easy','https://www.facebook.com/online2easy'),('Blog · Online2hobby','https://online2hobby.blogspot.com/')]
for lang in ['th','en']:
 th=lang=='th';prefix='' if th else '../';other='en/videos.html' if th else '../videos.html'
 title='วิดีโอสอนใช้งาน' if th else 'Video guides'
 heading='ดูวิธีติดตั้ง<br>แล้วค่อยลงมือทำ' if th else 'Watch the guide.<br>Then take the next step.'
 intro='เริ่มจากคลิปติดตั้งที่ผู้พัฒนาแนะนำ แล้วเปิดคู่มือกับหน้าดาวน์โหลดประกอบกัน วิดีโอเปิดบน YouTube ในแท็บใหม่ เพื่อให้กลับมาดูขั้นตอนบนเว็บนี้ได้เสมอ' if th else 'Start with the installation video recommended by the creator, alongside the written guide and downloads. Videos open on YouTube in a new tab so the project page stays available.'
 watch='ดูคลิปติดตั้งบน YouTube' if th else 'Watch the installation video'
 more='ดูเพลย์ลิสต์บน YouTube' if th else 'Open the YouTube playlist'
 unknown='คลิปนี้ยังไม่ระบุรุ่นที่ใช้ถ่าย โปรดเทียบขั้นตอนกับคู่มือของไฟล์ที่ดาวน์โหลด' if th else 'The version shown in this video has not been specified. Compare the steps with the guide for your downloaded package.'
 known=('รุ่นในคลิป: ' if th else 'Version in the video: ')+str(featured['version_in_video']) if featured['version_in_video'] else unknown
 developer='ผู้พัฒนา' if th else 'Developer'
 devlinks=' '.join(f'<a href="{u}" target="_blank" rel="noopener noreferrer">{label}</a>' for label,u in profiles)
 poster=f'''<a class="lesson-poster" data-video="featured" href="{url(featured)}" target="_blank" rel="noopener noreferrer" aria-label="{watch} ({'เปิดแท็บใหม่' if th else 'opens a new tab'})"><img src="{prefix}{featured['poster']}" width="960" height="540" alt="{'ภาพปกประกอบบทเรียนการติดตั้ง Thai-Menu' if th else 'Illustrated cover for the Thai-Menu installation lesson'}"></a>'''
 extra=''
 remaining=[v for v in items if v['id']!=catalog['featured']]
 if remaining:
  extra='<section class="section"><h2>'+('บทเรียนเพิ่มเติม' if th else 'More lessons')+'</h2><div class="lesson-grid">'
  for v in sorted(remaining,key=lambda x:x['added_at'],reverse=True):
   extra+=f'<article class="lesson-card"><h3>{esc(v["title"][lang])}</h3><p>{esc(v["summary"][lang])}</p><a href="{url(v)}" target="_blank" rel="noopener noreferrer">{("ดูบน YouTube" if th else "Watch on YouTube")}</a></article>'
  extra+='</div></section>'
 page=f'''<!doctype html>
<!-- Project learning pages; GPL-2.0-or-later. Preserve upstream notices. -->
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title} — FIRMWARE ADD-ON Thai-Menu</title><meta name="description" content="{esc(intro)}"><link rel="icon" href="{prefix}assets/icon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}assets/site.css?v={css}"><link rel="alternate" hreflang="{'en' if th else 'th'}" href="{other}"></head>
<body><a class="skip" href="#main">{'ข้ามไปเนื้อหา' if th else 'Skip to content'}</a><header class="top"><div class="wrap top-inner"><a class="brand" href="./"><span class="mark" aria-hidden="true">+</span><span><strong>EOS 600D</strong><small>FIRMWARE ADD-ON</small></span></a><nav aria-label="{'เมนูหลัก' if th else 'Main navigation'}"><a href="./">{'หน้าหลัก' if th else 'Home'}</a><a href="download.html">{'ดาวน์โหลด' if th else 'Download'}</a><a href="./#creator">{developer}</a><a class="language" href="{other}" lang="{'en' if th else 'th'}">{'English' if th else 'ภาษาไทย'}</a></nav></div></header>
<main id="main" class="wrap"><section class="section learning-intro"><div class="eyebrow">LEARN WITH THE CREATOR</div><h1>{heading}</h1><p>{intro}</p><p class="fine">{'โครงการสำหรับ Canon EOS 600D / Canon firmware 1.0.2 เท่านั้น ตรวจรุ่นกล้องและอ่านคู่มือก่อนติดตั้ง' if th else 'The project targets Canon EOS 600D / Canon firmware 1.0.2 only. Check your camera and read the installation guide first.'}</p></section>
<section class="section featured-lesson" id="installation" aria-labelledby="installation-title">{poster}<div class="lesson-copy"><span class="eyebrow">{'เริ่มต้นที่นี่ · คลิปติดตั้ง' if th else 'START HERE · INSTALLATION'}</span><h2 id="installation-title">{esc(featured['title'][lang])}</h2><p>{esc(featured['summary'][lang])}</p><div class="actions"><a class="button primary" data-video="watch" href="{url(featured)}" target="_blank" rel="noopener noreferrer">{watch}</a><a class="button" href="download.html">{'เลือกไฟล์ดาวน์โหลด' if th else 'Choose your download'}</a></div><p class="fine">{esc(known)}</p></div></section>
{extra}<section class="section playlist-panel" id="playlist"><div><div class="eyebrow">KEEP LEARNING</div><h2>{'คลิปใหม่ รวมไว้ในเพลย์ลิสต์เดียว' if th else 'Keep the playlist close at hand.'}</h2><p>{'เปิดเพลย์ลิสต์ของผู้พัฒนาเพื่อเลือกดูวิดีโออื่นและติดตามบทเรียนที่เพิ่มภายหลัง' if th else 'Open the creator’s playlist to explore other videos and follow lessons added later.'}</p></div><a class="button playlist-button" data-video="playlist" href="{esc(catalog['playlist_url'],quote=True)}" target="_blank" rel="noopener noreferrer">{more}</a></section>
<section class="section lesson-next"><h2>{'ดูคลิปแล้ว เริ่มตรงไหนดี?' if th else 'Ready for the next step?'}</h2><p>{'ยังไม่มี Magic Lantern เลือกชุด FIRST-INSTALL ถ้ามีอยู่แล้วเลือก UPDATE ส่วน Source เป็นไฟล์สำหรับผู้พัฒนา อ่านขั้นตอนติดตั้งบนหน้าดาวน์โหลดควบคู่กับวิดีโอ' if th else 'Choose FIRST-INSTALL if Magic Lantern is new to your camera, or UPDATE if it is already installed. Source code is for developers. Keep the written installation steps available alongside the video.'}</p><a class="button" href="download.html#first-install-steps">{'อ่านขั้นตอนติดตั้ง' if th else 'Read installation steps'}</a></section></main>
<footer class="footer wrap"><p><a href="./">{'หน้าหลัก' if th else 'Home'}</a> · <a href="download.html">{'ดาวน์โหลด' if th else 'Downloads'}</a></p><div class="developer-links"><strong>{developer}:</strong> {devlinks}</div><p class="disclosure">Independent Codex/LLM-assisted fork. Preserve Magic Lantern credits and licenses. Video guidance is not evidence that this firmware version passed hardware testing.</p></footer></body></html>
'''
 (docs/('videos.html' if th else 'en/videos.html')).write_text(page)
 homepage=docs/('index.html' if th else 'en/index.html');s=homepage.read_text()
 feature=f'''<!-- VIDEO_FEATURE --><section class="section video-feature" id="video-guide" aria-labelledby="video-guide-title"><div><div class="eyebrow">WATCH BEFORE YOU BEGIN</div><h2 id="video-guide-title">{'ดูคลิปติดตั้ง<br>ก่อนเริ่มใช้งาน' if th else 'Start with the<br>installation video.'}</h2><p>{'มีวิดีโอจากผู้พัฒนาให้ดูประกอบคู่มือ เปิดบน YouTube ในแท็บใหม่ แล้วกลับมาเลือกไฟล์ที่ตรงกับกล้องของคุณ' if th else 'Watch the creator’s installation guide on YouTube in a new tab, then return to choose the right package for your camera.'}</p><div class="actions"><a class="button" href="videos.html">{title}</a><a class="text-link" href="{url(featured)}" target="_blank" rel="noopener noreferrer">{'ดูคลิปบน YouTube ↗' if th else 'Watch on YouTube ↗'}</a></div></div><a class="lesson-poster" href="videos.html#installation"><img src="{prefix}{featured['poster']}" width="960" height="540" loading="lazy" alt="{'ไปหน้าวิดีโอสอนการติดตั้ง' if th else 'Open the installation video guide'}"></a></section><!-- /VIDEO_FEATURE -->'''
 if '<!-- VIDEO_FEATURE -->' in s:s=re.sub(r'<!-- VIDEO_FEATURE -->.*?<!-- /VIDEO_FEATURE -->',feature,s,flags=re.S)
 else:
  marker='<section class="section story"';assert marker in s;s=s.replace(marker,feature+'\n'+marker,1)
 homepage.write_text(s)
# Keep a video-library entry in every page's existing header navigation.
for p in docs.glob('**/*.html'):
 s=p.read_text();th='<html lang="th"' in s
 target=docs/('videos.html' if th else 'en/videos.html');href=os.path.relpath(target,p.parent).replace(os.sep,'/')
 def add_nav(m):
  nav=m.group(0)
  if f'href="{href}"' in nav:return nav
  link=f'<a href="{href}">{"วิดีโอ" if th else "Videos"}</a>'
  return nav.replace('<a class="language"',link+'<a class="language"',1)
 p.write_text(re.sub(r'<nav\b.*?</nav>',add_nav,s,flags=re.S))
print('Rendered bilingual video pages and homepage cards from website-content/videos.json')
