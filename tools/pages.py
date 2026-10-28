#!/usr/bin/env python3
"""Builds services.html, gallery.html, about-us.html, contact-us.html and sitemap.xml from site/index.html.
Run automatically by bump.sh. Edit index.html only; do not edit the generated pages by hand."""
import re,datetime
S='site/'
idx=open(S+'index.html').read()
BASE='https://www.gurucadd.com/'
i_main=idx.index('<main id="top">')+len('<main id="top">')
head=idx[:i_main]
i_first=idx.index('<section id="services">')
i_end=idx.index('</main>')
body=idx[i_first:i_end]
tail=idx[i_end:]
def sec(start_marker,end_marker):
    a=body.index(start_marker);b=body.index(end_marker,a)+len(end_marker);return body[a:b]
services=sec('<section id="services">','</section>')
gallery=sec('<section class="soft" id="gallery">','</section>')
lightbox=sec('<div class="lb" id="lb"','</div>\n')  # up to first closing div line
lb_a=body.index('<div class="lb" id="lb"');lb_b=body.index('</figure>\n</div>',lb_a)+len('</figure>\n</div>');lightbox=body[lb_a:lb_b]
industries=sec('<section id="industries">','</section>')
cases=sec('<section class="soft" id="cases">','</section>')
taskflow=sec('<section id="taskflow"','</section>')
process=sec('<section id="process">','</section>')
m=re.search(r'<section class="soft">\s*<div class="wrap">\s*<div class="head">\s*<div class="t"><span class="kicker">Software',body)
a=m.start();software=body[a:body.index('</section>',a)+10]
about=sec('<section id="about">','</section>')
contact=body[body.index('<div class="help on-navy" id="contact">'):]
PAGES=[
 ('services.html','Services','Our services','Production drawings, conceptual sales drawings, ERP integration and light gauge modular building design.','What we do',services+process+software),
 ('gallery.html','Drawing samples','Drawing samples','Real production, conceptual and modular drawing sheets from GuruCADD projects.','Our work',gallery+lightbox),
 ('about-us.html','About us','About GuruCADD','A Khulna drawing office of architects, engineers and ERP specialists, with industries served and case studies.','Who we are',about+industries+cases+taskflow),
 ('contact-us.html','Contact','Contact us','Send a sketch or project details and get a free quote from GuruCADD, Khulna, Bangladesh.','Get in touch',contact),
]
def fix(h):
    h=h.replace('href="#top"','href="index.html"')
    return re.sub(r'href="#([a-z]+)"',r'href="index.html#\1"',h)
for fn,t,h1,desc,kick,content in PAGES:
    hd=head
    hd=re.sub(r'<title>.*?</title>',f'<title>{t} | GuruCADD</title>',hd,1,flags=re.S)
    hd=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{desc}">',hd,1)
    hd=re.sub(r'<meta property="og:title" content="[^"]*">',f'<meta property="og:title" content="{t} | GuruCADD">',hd,1)
    hd=re.sub(r'<link rel="canonical"[^>]*>','',hd)
    hd=hd.replace('</head>',f'<link rel="canonical" href="{BASE}{fn}">\n</head>',1)
    band=f'\n<div class="pgh on-navy"><div class="wrap"><span class="kicker">{kick}</span><h1>{h1}</h1><p>{desc}</p></div></div>\n\n'
    page=fix(hd+band+content+'\n'+tail)
    # first section after the band should not look cramped; scripts tolerate missing elements
    page=page.replace("const $=id=>document.getElementById(id);","const $=id=>document.getElementById(id)||document.createElement('div');")
    open(S+fn,'w').write(page)
today=datetime.date.today().isoformat()
urls=['']+[p[0] for p in PAGES]
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{BASE}{u}</loc><lastmod>{today}</lastmod></url>\n' for u in urls)+'</urlset>\n'
open(S+'sitemap.xml','w').write(sm)
print('pages built')
