# -*- coding: utf-8 -*-
"""
Restyle the brief to the weatherkids.org direction, and add the new section
answering "what is new, exactly".

Design read from the reference (colours sampled from the live site):
  ground   rgb(48,80,97)  #305061   deep slate-blue sky
  accent   rgb(254,225,123) #FEE17B  butter yellow
  ink      rgb(43,51,63)  #2B333F
  display  SohneBreit (a wide grotesque)  -> Archivo at wdth 118
  body     ProximaNova                    -> Nunito Sans

Adapted rather than copied: the clouds are drawn here as blurred ellipse
clusters, not lifted from their site; the reflectivity ramp stays for data,
because it means something in this document; and the yellow is darkened to
--mark wherever it has to sit on a white card, since yellow on white fails
contrast.

The content sits on white sheets floating over the sky, which is what keeps a
15-section reading document legible on a saturated ground.
"""
import io
import re
import sys

P = "index.html"
s = io.open(P, encoding="utf-8").read()

# ════════════════════════════════════════════════════════════ 1. fonts
OLD_FONTS = re.search(r'<link rel="stylesheet" href="https://fonts\.googleapis[^>]*>', s)
if not OLD_FONTS:
    sys.exit("font link not found")
NEW_FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
             'family=Archivo:wdth,wght@75..125,400..800'
             '&family=Nunito+Sans:wght@300;400;600;700;900'
             '&family=IBM+Plex+Mono:wght@400;500;600'
             '&family=Tajawal:wght@400;500;700;800&display=swap">')
s = s.replace(OLD_FONTS.group(0), NEW_FONTS)

# ════════════════════════════════════════════════════════════ 2. stylesheet
NEW_CSS = r"""
/* ════════════════════════════════════════════════════════════════
   TOKENS — one sky, two times of day.

   Ground and accent are sampled from weatherkids.org (#305061 / #FEE17B).
   The reflectivity ramp is kept for DATA only: those five colours are what
   a meteorologist reads as 12/18/24/32 dBZ, the exact thresholds this brief
   reports, so they carry meaning the sky palette cannot.

   Yellow is unreadable on white, so --mark is the darkened form used for
   annotation on the white sheets, and --sun is used only over the sky.
   Every token is declared in bare :root so the system-theme document
   resolves correctly.
   ════════════════════════════════════════════════════════════════ */
:root{
  --sky0:#2A4557; --sky1:#305061; --sky2:#41708A; --sky3:#77A9C4;
  --cloud:#FFFFFF; --cloud-op:.34;

  --card:#FFFFFF; --card2:#F1F7FA;
  --ink:#22303B; --body:#4C5C68; --muted:#7C8B97; --faint:#A9B7C1;
  --rule:#DEE8EE; --rule2:#C2D2DC;

  --onsky:#FFFFFF; --onsky-dim:#CBDDE8;
  --sun:#FEE17B; --sun-deep:#E8B93C; --sun-soft:#FFF6DA;
  --mark:#C2510C;

  --dbz12:#2E86B8; --dbz18:#2C8A52; --dbz24:#C08E14; --dbz32:#C4581F; --dbzhi:#A32C1E;

  --shadow:0 1px 2px rgba(12,32,44,.06), 0 10px 30px -14px rgba(12,32,44,.28);
  --shadow-l:0 2px 6px rgba(12,32,44,.10), 0 26px 60px -22px rgba(12,32,44,.42);
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --sky0:#0C1820; --sky1:#13232D; --sky2:#1D3B4B; --sky3:#2E5B72;
    --cloud:#8FB6CB; --cloud-op:.13;
    --card:#182631; --card2:#1F2F3B;
    --ink:#EAF2F7; --body:#B6C6D0; --muted:#8296A3; --faint:#5F7280;
    --rule:#2B3D49; --rule2:#3C5261;
    --onsky:#EAF2F7; --onsky-dim:#93AAB8;
    --sun:#FCD968; --sun-deep:#E0B740; --sun-soft:#33301E;
    --mark:#F08A4B;
    --dbz12:#5FB4E2; --dbz18:#52B276; --dbz24:#EFC44E; --dbz32:#EC8047; --dbzhi:#DE5C48;
    --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 30px -14px rgba(0,0,0,.6);
    --shadow-l:0 2px 6px rgba(0,0,0,.45), 0 26px 60px -22px rgba(0,0,0,.7);
  }
}
:root[data-theme="dark"]{
  --sky0:#0C1820; --sky1:#13232D; --sky2:#1D3B4B; --sky3:#2E5B72;
  --cloud:#8FB6CB; --cloud-op:.13;
  --card:#182631; --card2:#1F2F3B;
  --ink:#EAF2F7; --body:#B6C6D0; --muted:#8296A3; --faint:#5F7280;
  --rule:#2B3D49; --rule2:#3C5261;
  --onsky:#EAF2F7; --onsky-dim:#93AAB8;
  --sun:#FCD968; --sun-deep:#E0B740; --sun-soft:#33301E;
  --mark:#F08A4B;
  --dbz12:#5FB4E2; --dbz18:#52B276; --dbz24:#EFC44E; --dbz32:#EC8047; --dbzhi:#DE5C48;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 30px -14px rgba(0,0,0,.6);
  --shadow-l:0 2px 6px rgba(0,0,0,.45), 0 26px 60px -22px rgba(0,0,0,.7);
}

*{box-sizing:border-box}
html{scroll-behavior:smooth; scroll-padding-top:96px}
body{
  margin:0; color:var(--onsky-dim);
  font:400 16.5px/1.72 "Nunito Sans","Segoe UI",system-ui,sans-serif;
  -webkit-font-smoothing:antialiased;
  background:var(--sky1);
  background-image:linear-gradient(180deg,var(--sky0) 0%,var(--sky1) 30%,var(--sky2) 68%,var(--sky3) 100%);
  background-attachment:fixed;
}
html[dir=rtl] body{font-family:"Tajawal","IBM Plex Sans Arabic",Tahoma,sans-serif; line-height:1.95}
@media (prefers-reduced-motion:reduce){*{animation:none!important; transition:none!important}}

body.lang-en .ar{display:none!important}
body.lang-ar .en{display:none!important}

/* ════════════════════ drifting cloud field ════════════════════
   Drawn here as blurred ellipse clusters — the reference's clouds are
   photographic and are not reused. They sit behind the white sheets, so
   they read in the gaps without ever competing with running text. */
.sky{position:fixed; inset:0; z-index:0; pointer-events:none; overflow:hidden}
.sky svg{position:absolute; fill:var(--cloud); opacity:var(--cloud-op); filter:blur(7px)}
.cl1{width:min(760px,88vw); top:5%;  left:-10%}
.cl2{width:min(620px,74vw); top:34%; right:-14%}
.cl3{width:min(880px,96vw); bottom:-6%; left:-6%; opacity:calc(var(--cloud-op) * 1.5)}
.cl4{width:min(520px,64vw); top:64%; left:4%}
@keyframes drift{from{transform:translateX(0)} to{transform:translateX(46px)}}
.cl1{animation:drift 34s ease-in-out infinite alternate}
.cl2{animation:drift 46s ease-in-out infinite alternate-reverse}
.cl3{animation:drift 62s ease-in-out infinite alternate}
.cl4{animation:drift 40s ease-in-out infinite alternate-reverse}

/* ════════════════════ top bar ════════════════════ */
#prog{position:fixed; inset-inline-start:0; top:0; height:3px; width:0; background:var(--sun); z-index:70}
#bar{position:sticky; top:0; z-index:60; padding:12px 18px 0}
#barin{
  max-width:1120px; margin:0 auto; display:flex; align-items:center; gap:12px;
  background:var(--card); border:1px solid var(--rule); border-radius:999px;
  padding:7px 8px 7px 20px; box-shadow:var(--shadow-l);
}
html[dir=rtl] #barin{padding:7px 20px 7px 8px}
#brand{
  font-family:"IBM Plex Mono",monospace; font-size:11px; font-weight:600;
  letter-spacing:1.6px; text-transform:uppercase; color:var(--ink); white-space:nowrap;
}
#brand i{color:var(--sun-deep); font-style:normal}
#jump{flex:1; min-width:0}
#sel{
  width:100%; max-width:330px; background:transparent; color:var(--body);
  border:0; border-inline-start:1px solid var(--rule);
  padding:4px 12px; font-family:inherit; font-size:13.5px; cursor:pointer;
}
#sel:focus-visible{outline:2px solid var(--mark); outline-offset:3px; border-radius:6px}
.langbtns{display:flex; gap:3px; background:var(--card2); border-radius:999px; padding:3px}
.langbtns button{
  background:transparent; color:var(--muted); border:0; padding:6px 15px; border-radius:999px;
  font-family:"IBM Plex Mono",monospace; font-size:11.5px; font-weight:600; cursor:pointer;
  letter-spacing:.8px; transition:background .18s,color .18s;
}
.langbtns button.on{background:var(--ink); color:var(--card)}
.langbtns button:focus-visible{outline:2px solid var(--mark); outline-offset:2px}

/* ════════════════════ layout — white sheets on the sky ════════════════════ */
main{max-width:1120px; margin:0 auto; padding:0 22px 90px; position:relative; z-index:1}
section{
  background:var(--card); border-radius:30px; padding:48px 44px 40px;
  margin:0 0 30px; box-shadow:var(--shadow-l); position:relative;
}
#hero{background:none; box-shadow:none; padding:22px 0 8px}
@media (max-width:600px){section{padding:34px 24px 30px; border-radius:24px}}

h1,h2{color:var(--ink); text-wrap:balance; margin:0}
h1,h2,h3,.k3d-bar .lbl,.stats .n{font-variation-settings:"wdth" 116}
h1{
  font-family:"Archivo","Segoe UI",sans-serif; font-weight:700;
  font-size:clamp(33px,5.6vw,58px); line-height:1.06; letter-spacing:-1.4px; margin-bottom:18px;
}
h2{
  font-family:"Archivo","Segoe UI",sans-serif; font-weight:700;
  font-size:clamp(24px,3.6vw,36px); line-height:1.16; letter-spacing:-.8px; margin-bottom:10px;
}
h3{
  font-family:"Archivo","Segoe UI",sans-serif; font-size:20px; font-weight:700;
  color:var(--ink); margin:38px 0 10px; letter-spacing:-.4px;
}
html[dir=rtl] h1,html[dir=rtl] h2,html[dir=rtl] h3{
  font-family:"Tajawal","IBM Plex Sans Arabic",sans-serif; font-weight:800;
  letter-spacing:0; font-variation-settings:normal;
}
html[dir=rtl] h1{line-height:1.4} html[dir=rtl] h2{line-height:1.5} html[dir=rtl] h3{line-height:1.6}
p{margin:0 0 15px; max-width:68ch; color:var(--body)}
.lead{font-size:19px; line-height:1.62; max-width:58ch}
a{color:var(--mark)}

.eyebrow{
  font-family:"IBM Plex Mono",monospace; font-size:11px; font-weight:500;
  letter-spacing:2.6px; text-transform:uppercase; color:var(--muted);
  margin-bottom:14px; display:flex; align-items:center; gap:11px;
}
.eyebrow::before{content:""; width:26px; height:1px; background:var(--rule2); flex:none}
.eyebrow b{color:var(--mark); font-weight:600}

/* ════════════════════ hero ════════════════════ */
.scope{
  position:relative; border-radius:30px; overflow:hidden;
  background:linear-gradient(170deg,#5E93B4,#3C6885 52%,#2C4A5C);
  box-shadow:var(--shadow-l); padding:38px 38px 96px; margin-bottom:18px;
}
.scope h1{color:#FFFFFF}
.scope .lead{color:#D8E9F3}
.scope .lead b,.scope h1 i{color:var(--sun); font-style:normal}
.radar{position:absolute; inset-inline-end:-38px; top:-34px; width:330px; height:330px; opacity:.34}
html[dir=rtl] .radar{transform:scaleX(-1)}
.herocloud{position:absolute; left:-4%; right:-4%; bottom:-14px; width:108%; fill:#FFFFFF; opacity:.9}
.scope-in{position:relative; z-index:2}
.tag{
  display:inline-flex; align-items:center; gap:8px; font-family:"IBM Plex Mono",monospace;
  font-size:10.5px; font-weight:600; letter-spacing:2px; text-transform:uppercase;
  color:#2B333F; background:var(--sun); padding:7px 16px; border-radius:999px; margin-bottom:20px;
}
.tag i{width:6px; height:6px; border-radius:50%; background:#2B333F; font-style:normal}
html[dir=rtl] .tag{font-family:"Tajawal",sans-serif; letter-spacing:0; font-size:12px}

/* ════════════════════ stat strip ════════════════════ */
.stats{
  display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr));
  border:1px solid var(--rule); border-radius:20px; overflow:hidden;
  background:var(--card); box-shadow:var(--shadow); margin:22px 0;
}
#hero .stats{box-shadow:var(--shadow-l); border:0}
.stats>div{padding:20px; border-inline-start:1px solid var(--rule)}
.stats>div:first-child{border-inline-start:0}
.stats .n{
  font-family:"Archivo",sans-serif; font-size:27px; font-weight:800;
  letter-spacing:-1.2px; line-height:1.15; direction:ltr; font-variant-numeric:tabular-nums;
}
.stats .l{font-size:13px; line-height:1.5; color:var(--muted); margin-top:6px}
.c12{color:var(--dbz12)} .c18{color:var(--dbz18)} .c24{color:var(--dbz24)}
.c32{color:var(--dbz32)} .chi{color:var(--dbzhi)}

/* ════════════════════ the annotation pen ════════════════════ */
.pen{
  display:inline-flex; align-items:center; gap:6px; font-family:"IBM Plex Mono",monospace;
  font-size:10.5px; font-weight:600; letter-spacing:1.7px; text-transform:uppercase;
  color:var(--mark); margin-inline-start:12px; vertical-align:middle; white-space:nowrap;
}
.pen svg{width:15px; height:15px; flex:none; fill:none; stroke:currentColor;
  stroke-width:2.4; stroke-linecap:round; stroke-linejoin:round}
html[dir=rtl] .pen svg{transform:scaleX(-1)}
html[dir=rtl] .pen{font-family:"Tajawal",sans-serif; letter-spacing:0; font-size:12px}
.pen.grey{color:var(--muted)}

.thread{display:none}

/* ════════════════════ blocks ════════════════════ */
.note{
  background:var(--card2); border:1px solid var(--rule); border-radius:20px;
  padding:24px 26px; margin:20px 0;
}
.note h4{
  font-family:"Archivo",sans-serif; font-size:18px; font-weight:700; color:var(--ink);
  margin:0 0 10px; letter-spacing:-.3px; font-variation-settings:"wdth" 112;
}
html[dir=rtl] .note h4{font-family:"Tajawal",sans-serif; font-weight:800; letter-spacing:0; font-variation-settings:normal}
.note p:last-child,.note ul:last-child,.note ol:last-child{margin-bottom:0}
.note.key{background:var(--sun-soft); border-color:var(--sun-deep)}
.note.key h4{color:var(--mark)}
.note.flat{background:transparent; border-style:dashed}
.note.warn{border-color:var(--mark); background:var(--card)}

.grid{display:grid; gap:18px; margin:22px 0}
.g2{grid-template-columns:repeat(auto-fit,minmax(272px,1fr))}
.g3{grid-template-columns:repeat(auto-fit,minmax(212px,1fr))}
.g4{grid-template-columns:repeat(auto-fit,minmax(180px,1fr))}

.step{border-top:3px solid var(--ink); padding-top:14px}
.step.hot{border-top-color:var(--mark)}
.step .no{
  font-family:"IBM Plex Mono",monospace; font-size:10.5px; font-weight:600;
  letter-spacing:2px; color:var(--mark); text-transform:uppercase; margin-bottom:7px;
}
.step h4{font-family:"Archivo",sans-serif; font-size:17px; color:var(--ink); margin:0 0 7px;
  font-weight:700; letter-spacing:-.2px}
html[dir=rtl] .step h4{font-family:"Tajawal",sans-serif; font-weight:800; letter-spacing:0}
.step p{font-size:15px; margin:0; color:var(--body); max-width:none}

.say{
  border:1px solid var(--sun-deep); border-inline-start:5px solid var(--sun-deep);
  background:var(--sun-soft); border-radius:0 20px 20px 0; padding:24px 28px; margin:22px 0;
}
html[dir=rtl] .say{border-radius:20px 0 0 20px}
.say .who{
  display:block; font-family:"IBM Plex Mono",monospace; font-size:10.5px; font-weight:600;
  letter-spacing:2px; text-transform:uppercase; color:var(--mark); margin-bottom:11px;
}
html[dir=rtl] .say .who{font-family:"Tajawal",sans-serif; letter-spacing:0; font-size:12.5px}
.say .q{
  display:block; font-family:"Archivo",sans-serif; font-size:19.5px; line-height:1.52;
  color:var(--ink); font-weight:500; max-width:62ch; font-variation-settings:"wdth" 106;
}
html[dir=rtl] .say .q{font-family:"Tajawal",sans-serif; font-size:18px; line-height:1.9;
  font-weight:500; font-variation-settings:normal}

/* ════════════════════ tables ════════════════════ */
.tw{overflow-x:auto; margin:20px 0; border:1px solid var(--rule); border-radius:18px; background:var(--card)}
table{border-collapse:collapse; width:100%; font-size:14.5px; min-width:460px}
th,td{padding:13px 16px; text-align:start; border-bottom:1px solid var(--rule); color:var(--body)}
th{
  font-family:"IBM Plex Mono",monospace; font-size:10.5px; letter-spacing:1.4px;
  text-transform:uppercase; color:var(--muted); font-weight:500; background:var(--card2);
}
html[dir=rtl] th{font-family:"Tajawal",sans-serif; letter-spacing:0; font-size:12.5px}
tr:last-child td{border-bottom:0}
td b{color:var(--ink)}
tr.hi td{background:var(--sun-soft)}
tr.hi td b{color:var(--mark)}
.mono{font-family:"IBM Plex Mono",monospace; font-variant-numeric:tabular-nums; direction:ltr; display:inline-block}
.ok{color:var(--dbz18)} .todo{color:var(--muted)}

/* ════════════════════ figures ════════════════════ */
figure{
  margin:26px 0; background:var(--card); border:1px solid var(--rule); border-radius:22px;
  padding:24px 20px 16px; direction:ltr; overflow-x:auto;
}
figure svg.plot{display:block; width:100%; min-width:440px; height:auto}
figcaption{
  margin:15px auto 0; font-size:14px; line-height:1.65; color:var(--muted);
  max-width:74ch; text-align:center;
}
html[dir=rtl] figcaption{direction:rtl; font-size:14.5px}

/* ════════════════════ misc ════════════════════ */
ul,ol{margin:0 0 15px; padding-inline-start:22px; max-width:68ch; color:var(--body)}
li{margin-bottom:9px}
li::marker{color:var(--mark)}
code{
  font-family:"IBM Plex Mono",monospace; background:var(--card2); padding:2px 7px;
  border-radius:5px; font-size:13px; color:var(--ink); direction:ltr;
}
.gloss{display:grid; grid-template-columns:minmax(116px,180px) 1fr; margin:18px 0; font-size:15px}
.gloss dt{
  font-family:"IBM Plex Mono",monospace; font-size:13px; font-weight:500; color:var(--ink);
  padding:10px 0; border-top:1px solid var(--rule);
}
html[dir=rtl] .gloss dt{font-family:"Tajawal",sans-serif; font-size:14.5px; font-weight:700}
.gloss dd{margin:0; padding:10px 0 10px 18px; border-top:1px solid var(--rule); color:var(--body)}
html[dir=rtl] .gloss dd{padding:10px 18px 10px 0}
.src{font-family:"IBM Plex Mono",monospace; font-size:10.5px; letter-spacing:1px; color:var(--muted); margin:0 0 10px}
footer{
  max-width:1120px; margin:0 auto; padding:14px 22px 70px; position:relative; z-index:1;
  font-family:"IBM Plex Mono",monospace; font-size:11px; line-height:1.9; color:var(--onsky-dim);
}
html[dir=rtl] footer{font-family:"Tajawal",sans-serif; font-size:12.5px}
footer code{background:rgba(255,255,255,.14); color:var(--onsky)}

/* ════════════════════════════════════════════════════════════════
   MOTION — one ambient loop, one arrival per section, hover feedback.
   Gated behind .js, so with scripting off the page renders complete and
   still. The hero and section 01 never reveal, so the first frame is
   always fully readable.
   ════════════════════════════════════════════════════════════════ */
@keyframes sweep{to{transform:rotate(360deg)}}
@keyframes rise{from{opacity:0; transform:translateY(18px)} to{opacity:1; transform:none}}
@keyframes drawpen{from{stroke-dashoffset:46} to{stroke-dashoffset:0}}
@keyframes growY{from{transform:scaleY(0)} to{transform:scaleY(1)}}
@keyframes growX{from{transform:scaleX(0)} to{transform:scaleX(1)}}

.sweepg{transform-origin:100px 100px; animation:sweep 11s linear infinite}

.js .rv{opacity:0}
.js .rv.in{animation:rise .6s cubic-bezier(.22,.75,.3,1) both}

.js .rv .gb{transform-box:fill-box; transform-origin:bottom; transform:scaleY(0)}
.js .rv.in .gb{animation:growY .72s cubic-bezier(.2,.85,.3,1) both}
.js .rv.in .gb:nth-of-type(2){animation-delay:.06s}
.js .rv.in .gb:nth-of-type(3){animation-delay:.12s}
.js .rv.in .gb:nth-of-type(4){animation-delay:.18s}

.js .rv .gx{transform-box:fill-box; transform-origin:left; transform:scaleX(0)}
.js .rv.in .gx{animation:growX .8s cubic-bezier(.2,.85,.3,1) both}
.js .rv.in .gx.late{animation-delay:.22s}

.js .rv .pen svg path{stroke-dasharray:46; stroke-dashoffset:46}
.js .rv.in .pen svg path{animation:drawpen .65s .3s ease both}
.js .rv.in .pen svg path:last-child{animation-delay:.46s}

.note,.step{transition:transform .22s ease, box-shadow .22s ease, border-color .22s ease}
.note:hover{transform:translateY(-2px); box-shadow:var(--shadow)}
.step:hover{transform:translateY(-2px)}
table tr{transition:background .16s ease}
table tr:not(.hi):hover td{background:var(--card2)}
.langbtns button:hover{color:var(--ink)}
.langbtns button.on:hover{color:var(--card)}

main,footer{transition:opacity .16s ease}
body.swapping main,body.swapping footer{opacity:.25}

/* ════════════════════ the interactive kernel ════════════════════ */
.k3d{
  margin:26px 0; background:var(--card); border:1px solid var(--rule);
  border-radius:22px; overflow:hidden;
}
.k3d-bar{
  display:flex; align-items:center; gap:10px; flex-wrap:wrap;
  padding:16px 20px; border-bottom:1px solid var(--rule); background:var(--card2);
}
.k3d-bar .lbl{
  font-family:"IBM Plex Mono",monospace; font-size:10.5px; letter-spacing:1.8px;
  text-transform:uppercase; color:var(--muted); margin-inline-end:auto;
}
html[dir=rtl] .k3d-bar .lbl{font-family:"Tajawal",sans-serif; letter-spacing:0; font-size:12.5px}
.k3d-bar button{
  font-family:"IBM Plex Mono",monospace; font-size:11px; font-weight:600; letter-spacing:.6px;
  padding:9px 15px; border-radius:999px; cursor:pointer; background:var(--card);
  border:1px solid var(--rule2); color:var(--ink); transition:all .18s ease;
}
html[dir=rtl] .k3d-bar button{font-family:"Tajawal",sans-serif; font-size:13px}
.k3d-bar button:hover{border-color:var(--ink)}
.k3d-bar button:focus-visible{outline:2px solid var(--mark); outline-offset:2px}
.k3d-bar button.ok{border-color:var(--dbz18); color:var(--dbz18)}
.k3d-bar button.ok:hover{background:var(--dbz18); color:var(--card)}
.k3d-bar button.no{border-color:var(--dbzhi); color:var(--dbzhi)}
.k3d-bar button.no:hover{background:var(--dbzhi); color:var(--card)}
#kernel3d{display:block; width:100%; height:400px; cursor:grab; touch-action:pan-y}
#kernel3d:active{cursor:grabbing}
.k3d-note{
  padding:16px 20px; border-top:1px solid var(--rule); font-size:14px;
  line-height:1.6; color:var(--muted); min-height:62px;
}
.k3d-note b{color:var(--ink)}
.k3d-note.good b{color:var(--dbz18)}
.k3d-note.bad b{color:var(--dbzhi)}
.k3d-fallback{padding:22px 20px; font-size:14px; color:var(--muted)}

@media (prefers-reduced-motion:reduce){
  .sweepg,.sky svg{animation:none}
  .js .rv{opacity:1}
  .js .rv.in{animation:none}
  .js .rv .gb,.js .rv .gx{transform:none}
  .js .rv.in .gb,.js .rv.in .gx{animation:none}
  .js .rv .pen svg path{stroke-dashoffset:0}
  .js .rv.in .pen svg path{animation:none}
  .note:hover,.step:hover{transform:none}
}
"""

start = s.index("<style>") + len("<style>")
end = s.index("</style>")
s = s[:start] + NEW_CSS + s[end:]

# ════════════════════════════════════════════════════════════ 3. cloud field
CLOUD = '''<svg viewBox="0 0 640 240" class="%s" aria-hidden="true"><g>
<ellipse cx="300" cy="168" rx="252" ry="56"/><circle cx="176" cy="140" r="60"/>
<circle cx="262" cy="112" r="80"/><circle cx="362" cy="128" r="66"/>
<circle cx="452" cy="152" r="50"/><circle cx="112" cy="162" r="42"/></g></svg>'''
SKY = ('<div class="sky" aria-hidden="true">'
       + "".join(CLOUD % c for c in ("cl1", "cl2", "cl3", "cl4"))
       + '</div>\n')
anchor = '<div id="prog"></div>'
if s.count(anchor) != 1:
    sys.exit("prog anchor not unique")
s = s.replace(anchor, SKY + anchor)

# a cloud bank rising into the hero, the way the reference does it
HEROCLOUD = '''<svg class="herocloud" viewBox="0 0 1200 150" preserveAspectRatio="none" aria-hidden="true"><g>
<ellipse cx="600" cy="126" rx="640" ry="48"/><circle cx="250" cy="104" r="52"/>
<circle cx="360" cy="86" r="66"/><circle cx="500" cy="98" r="54"/><circle cx="700" cy="90" r="62"/>
<circle cx="850" cy="104" r="50"/><circle cx="980" cy="112" r="42"/><circle cx="130" cy="116" r="40"/>
</g></svg>'''
anchor = '    <div class="scope-in">'
if s.count(anchor) != 1:
    sys.exit("scope-in anchor not unique")
s = s.replace(anchor, "    " + HEROCLOUD + "\n" + anchor)

io.open(P, "w", encoding="utf-8").write(s)
print("restyled: fonts, %d chars of css, cloud field, hero cloud bank" % len(NEW_CSS))
