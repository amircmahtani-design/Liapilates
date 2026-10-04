"""Generate the LIA site pages from shared templates.

Writes static HTML (index.html, about/, method/, pilates/, mobility/,
neuromovement/, studio/, contact/, 404.html). Netlify serves the output as-is,
so there is no build step on deploy: edit here, run, commit.

Run:  python3 tools/build_pages.py
"""
from pathlib import Path

import build_brand

ROOT = Path(__file__).resolve().parent.parent

NAV = [
    ("/about/", "About Lia"),
    ("/method/", "The Method"),
    ("/pilates/", "Pilates"),
    ("/mobility/", "Mobility"),
    ("/neuromovement/", "Neuromovement"),
    ("/studio/", "Studio"),
    ("/contact/", "Contact"),
]

# Bump when images, CSS or JS change: browsers cache by URL, and an earlier
# build shipped placeholder images under the same file names.
V = "3"

ARROW = '<svg aria-hidden="true"><use href="#i-arrow"/></svg>'


# ---------------------------------------------------------------- building blocks
def pic(name, alt, w, h, style="", priority=False):
    """WebP with a JPEG fallback. Loaded eagerly: each page carries only a few photos."""
    attrs = ' fetchpriority="high"' if priority else ""
    st = f' style="{style}"' if style else ""
    return (f'<picture><source type="image/webp" srcset="/assets/images/{name}.webp?v={V}">'
            f'<img src="/assets/images/{name}.jpg?v={V}" alt="{alt}" width="{w}" height="{h}"{st}{attrs} decoding="async"></picture>')


IMG = {
    "hero": ("hero", "Lia holding a slow, controlled bridge on the reformer in a sunlit room", 1448, 1086),
    "pilates": ("pilates", "Lia guiding a client through reformer footwork, one hand resting on her knee", 1600, 900),
    "mobility": ("mobility-90-90", "Lia kneeling beside a client on a mat, guiding a controlled seated hip rotation", 1448, 1086),
    "neuromovement": ("neuromovement-coordination", "Lia steadying a client who balances on one leg on a cushion, reaching forward with the opposite arm", 1448, 1086),
    "portrait": ("lia-portrait", "Portrait of Lia, seated on a mat in her studio", 940, 1175),
    "studio": ("studio-wide", "The studio in afternoon light: a timber reformer on a jute rug, arched windows and palms outside", 1672, 941),
}


def img(key, style="", priority=False):
    name, alt, w, h = IMG[key]
    return pic(name, alt, w, h, style, priority)


CURRENT = ' aria-current="page"'


def page(path, title, description, body, preload=None):
    depth_nav = "\n".join(
        f'        <li><a href="{href}"{CURRENT if href == path else ""}>{label}</a></li>' for href, label in NAV)
    menu_nav = "\n".join(
        f'    <li><a href="{href}"{CURRENT if href == path else ""}>{label}</a></li>' for href, label in NAV)
    footer_nav = "\n".join(f'        <a href="{href}">{label}</a>' for href, label in NAV)
    pre = (f'<link rel="preload" as="image" href="/assets/images/{preload}.webp?v={V}" type="image/webp" fetchpriority="high">\n'
           if preload else "")
    sprite = build_brand.sprite() if path == "/" else ""
    canonical = "https://liapilates.netlify.app" + path
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#F8F6F2">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/assets/favicon/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/favicon/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="https://liapilates.netlify.app/assets/images/hero.jpg">
<meta property="og:type" content="website">
<link rel="preload" href="/assets/fonts/cormorant-garamond.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/manrope.woff2" as="font" type="font/woff2" crossorigin>
{pre}<link rel="stylesheet" href="/assets/site.css?v={V}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <defs>
{sprite}
    <symbol id="i-arrow" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M4 12h15.5M14 6.5l5.5 5.5-5.5 5.5"/></symbol>
  </defs>
</svg>

<header class="header" id="header">
  <div class="container header__in">
    <a class="brand" href="/" aria-label="LIA home">
      <img src="/assets/branding/lia-wordmark.svg" alt="LIA" width="66" height="44">
    </a>
    <nav class="nav" aria-label="Main">
      <ul>
{depth_nav}
      </ul>
    </nav>
    <a class="btn btn--secondary header__cta" href="/contact/">Book a session</a>
    <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="menu"><span></span></button>
  </div>
</header>

<div class="menu" id="menu">
  <ul>
{menu_nav}
  </ul>
  <div class="menu__foot">
    <a class="btn btn--primary" href="/contact/">Book a session</a>
    <p>Jumeirah Park, Dubai</p>
  </div>
</div>

<main id="main">
{body}
</main>

<footer class="footer">
  <div class="container">
    <div class="footer__top">
      <a class="footer__logo" href="/" aria-label="LIA home"><img src="/assets/branding/lia-wordmark-light.svg" alt="LIA" width="96" height="64"></a>
      <nav class="footer__nav" aria-label="Footer">
{footer_nav}
      </nav>
      <div class="footer__info">
        <p><strong>Jumeirah Park, Dubai</strong> Sessions by appointment</p>
      </div>
    </div>
    <div class="footer__bottom">
      <p>© <span id="year">2026</span> LIA</p>
      <p>Movement teaching, not medical treatment. Please check with your doctor about any medical condition.</p>
    </div>
  </div>
</footer>

<script src="/assets/site.js?v={V}" defer></script>
</body>
</html>
"""


CLOSING = """
<section class="section closing" aria-labelledby="closing-title">
  <div class="container closing__grid">
    <h2 id="closing-title" class="h1"><span class="line">Your body.</span> <span class="line">Your movement.</span> <span class="line">Your session.</span></h2>
    <div class="closing__action">
      <a class="btn btn--primary" href="/contact/">Book a private session</a>
      <p class="closing__place">Jumeirah Park, Dubai</p>
    </div>
  </div>
</section>"""

PRINCIPLES = """
<section class="principles" aria-label="Principles">
  <div class="container">
    <ul>
      <li class="principle"><svg aria-hidden="true"><use href="#b-personalised"/></svg><h3>Personalised</h3> <p>No two bodies move the same.</p></li>
      <li class="principle"><svg aria-hidden="true"><use href="#b-mobility"/></svg><h3>Mobility</h3> <p>Range you can actually use.</p></li>
      <li class="principle"><svg aria-hidden="true"><use href="#b-control"/></svg><h3>Control</h3> <p>Strength through precision.</p></li>
      <li class="principle"><svg aria-hidden="true"><use href="#b-connection"/></svg><h3>Connection</h3> <p>Brain and body working together.</p></li>
      <li class="principle"><svg aria-hidden="true"><use href="#b-longevity"/></svg><h3>Longevity</h3> <p>Habits that last for decades.</p></li>
    </ul>
  </div>
</section>"""

DISCIPLINES = {
    "pilates": dict(
        num="01", name="Pilates", statement="Strength. Control. Precision.", img="pilates", pos="40% 50%",
        short="Deliberate, unhurried work on the reformer and mat that builds deep strength and control without strain.",
        prose=[
            "Pilates is often where sessions begin, because it gives the body a stable base to work from.",
            "Exercises are chosen and adjusted for you, with attention on breath, alignment and the quality of each repetition rather than the number of them. The reformer supports and challenges in equal measure, so the work can be gentle or demanding depending on the day.",
        ],
        include=["Reformer footwork and bridging", "Side-lying and core control work", "Mat work you can repeat at home"],
        suits=["Building strength without strain", "Posture and everyday support", "A steady return to exercise"],
    ),
    "mobility": dict(
        num="02", name="Mobility", statement="Freedom you can use.", img="mobility", pos="50% 60%",
        short="Improve the range, control and confidence of the way you move day to day.",
        prose=[
            "Mobility work here isn’t about stretching further. It’s about owning the range you already have, then gently adding to it.",
            "Slow, controlled rotations of the hips, spine, shoulders and ankles make ordinary things easier: getting up off the floor, turning to look behind you, reaching for a high shelf without thinking about it.",
        ],
        include=["Hip rotation and 90/90 work", "Thoracic rotation and shoulder control", "Ankle and foot drills"],
        suits=["Stiffness and tight hips or back", "Long days at a desk", "Active adults who want to keep moving"],
    ),
    "neuromovement": dict(
        num="03", name="Neuromovement", statement="Reconnect. Re-educate. Rebalance.", img="neuromovement", pos="50% 35%",
        short="Focused tasks that challenge balance, coordination and awareness.",
        prose=[
            "Neuromovement uses slow, deliberate tasks that ask the brain and body to work together: standing on one leg, reaching across the body, finding your balance on a soft surface.",
            "It is quiet, focused work. Done well, it sharpens coordination and confidence on your feet, and often makes everything else in a session feel easier.",
        ],
        include=["Single-leg balance", "Cross-body coordination patterns", "Balance pad and small-ball work"],
        suits=["Feeling steadier on your feet", "Sharpening coordination at any age", "Adding variety to strength work"],
    ),
}


def tile(key):
    d = DISCIPLINES[key]
    return f"""      <article class="tile">
        <a class="tile__media" href="/{key}/" tabindex="-1" aria-hidden="true">{img(d['img'], style='object-position:' + d['pos'])}</a>
        <span class="tile__num">{d['num']}</span>
        <h3 class="h3"><a href="/{key}/">{d['name']}</a></h3>
        <p class="tile__statement">{d['statement']}</p>
        <p class="tile__text">{d['short']}</p>
        <a class="link" href="/{key}/">Explore {d['name']} {ARROW}</a>
      </article>"""


def next_list(exclude=None, heading="Other disciplines"):
    rows = []
    for key, d in DISCIPLINES.items():
        if key == exclude:
            continue
        rows.append(f"""      <li><a href="/{key}/"><span class="next-list__num">{d['num']}</span> <span class="next-list__name">{d['name']} <em>{d['statement']}</em></span> {ARROW}</a></li>""")
    return f"""
<section class="section" aria-labelledby="next-title" style="padding-top:0">
  <div class="container">
    <h2 id="next-title" class="eyebrow" style="margin-bottom:var(--space-5)">{heading}</h2>
    <ul class="next-list">
{chr(10).join(rows)}
    </ul>
  </div>
</section>"""


# ---------------------------------------------------------------- pages
def home():
    tiles = "\n".join(tile(k) for k in DISCIPLINES)
    body = f"""
<section class="hero" aria-labelledby="hero-title">
  <div class="container hero__grid">
    <div class="hero__copy">
      <p class="eyebrow">Private home studio · Jumeirah Park</p>
      <h1 id="hero-title" class="h1"><span class="line">Move better.</span> <span class="line">Live fuller.</span></h1>
      <p class="hero__sub">Pilates · Mobility · Neuromovement</p>
      <p class="lead">A deeply personalised approach to movement, designed around your body, your goals and the way you live.</p>
      <div class="hero__ctas">
        <a class="btn btn--primary" href="/contact/">Book a session</a>
        <a class="btn btn--secondary" href="/method/">Discover the method</a>
      </div>
    </div>
    <figure class="hero__media">{img('hero', priority=True)}</figure>
  </div>
</section>
{PRINCIPLES}

<section class="section" aria-labelledby="disc-title">
  <div class="container">
    <div class="section-intro">
      <div>
        <p class="eyebrow">Three disciplines</p>
        <h2 id="disc-title" class="h2">How Lia works</h2>
      </div>
      <p class="lead">Each has its own purpose. Most sessions combine all three, in the balance you need at the time.</p>
    </div>
    <div class="tiles">
{tiles}
    </div>
  </div>
</section>

<section class="section about" aria-labelledby="about-title" style="padding-top:0">
  <div class="container about__grid">
    <figure class="about__portrait">{img('portrait')}</figure>
    <div class="about__copy">
      <p class="eyebrow">About Lia</p>
      <h2 id="about-title" class="h2">Exercise is only part of it. <em>It’s how you feel in your body every day.</em></h2>
      <div class="prose">
        <p>Lia doesn’t begin with a list of exercises. She begins by watching how you stand, breathe, turn and carry yourself.</p>
      </div>
      <a class="link" href="/about/">More about Lia {ARROW}</a>
    </div>
  </div>
</section>

<section class="section studio" aria-labelledby="studio-title">
  <div class="container">
    <figure class="studio__media">{img('studio', style='object-position:45% 50%')}</figure>
    <div class="studio__text">
      <h2 id="studio-title" class="h2">A quieter way to train.</h2>
      <div>
        <p class="lead">Private sessions in a calm home studio in Jumeirah Park, with the time and space to focus entirely on you.</p>
        <a class="link" href="/studio/">See the studio {ARROW}</a>
      </div>
    </div>
  </div>
</section>
{CLOSING}"""
    return page("/", "LIA — Pilates, Mobility &amp; Neuromovement · Jumeirah Park, Dubai",
                "One-to-one Pilates, mobility and neuromovement sessions with Lia, in a calm home studio in Jumeirah Park, Dubai.",
                body, preload="hero")


def about():
    body = f"""
<section class="section about" aria-labelledby="about-title">
  <div class="container about__grid">
    <figure class="about__portrait">
      {img('portrait', priority=True)}
      <figcaption>Lia, founder and teacher</figcaption>
    </figure>
    <div class="about__copy">
      <p class="eyebrow">About Lia</p>
      <h1 id="about-title" class="h2">Exercise is only part of it. <em>It’s how you feel in your body every day.</em></h1>
      <div class="prose">
        <p>Lia doesn’t begin with a list of exercises. She begins by watching how you stand, breathe, turn and carry yourself.</p>
        <p>Years of working with clients of different ages, goals and histories have shaped the way she teaches. The same exercise can help one person and do little for the next, so each session draws on Pilates, mobility and neuromovement in whatever proportion suits you that day.</p>
        <p>The aim is simple: to help you feel stronger, move more freely and trust your body again.</p>
      </div>
    </div>
  </div>
</section>

<section class="section experience" aria-labelledby="exp-title" style="padding-top:0">
  <div class="container">
    <h2 id="exp-title" class="eyebrow">Experience</h2>
    <div class="facts">
      <p class="fact"><span class="fact__n">10+</span> <span class="fact__label">Years of experience</span></p>
      <p class="fact"><span class="fact__n">1:1</span> <span class="fact__label">Personal attention</span></p>
      <p class="fact"><span class="fact__n">100%</span> <span class="fact__label">Individual approach</span></p>
    </div>
    <figure class="quote">
      <blockquote><p>“Experience changes the way you see movement. You stop asking everyone to move the same way.”</p></blockquote>
      <figcaption>Lia</figcaption>
    </figure>
  </div>
</section>

<section class="section who" aria-labelledby="who-title" style="background:var(--sand)">
  <div class="container">
    <h2 id="who-title" class="h2"><span class="line">You don’t need to be flexible.</span> <span class="line">You just need to start where you are.</span></h2>
    <div class="who__grid">
      <div class="who__intro">
        <p class="lead">Lia works with adults of all ages and starting points. Sessions are paced to you, never a performance and never a competition.</p>
        <a class="link" href="/contact/">Arrange a first session {ARROW}</a>
      </div>
      <ol class="who__list">
        <li><span class="who__num" aria-hidden="true">i</span> <span class="who__text">Anyone who simply wants to move better</span></li>
        <li><span class="who__num" aria-hidden="true">ii</span> <span class="who__text">People who feel stiff, tight or stuck</span></li>
        <li><span class="who__num" aria-hidden="true">iii</span> <span class="who__text">Active adults who want to keep doing what they love</span></li>
        <li><span class="who__num" aria-hidden="true">iv</span> <span class="who__text">Anyone returning to exercise after time away</span></li>
        <li><span class="who__num" aria-hidden="true">v</span> <span class="who__text">Those who want strength without aggressive training</span></li>
        <li><span class="who__num" aria-hidden="true">vi</span> <span class="who__text">Older clients who want to keep moving well</span></li>
      </ol>
    </div>
  </div>
</section>
{CLOSING}"""
    return page("/about/", "About Lia — LIA Pilates, Mobility &amp; Neuromovement",
                "How Lia teaches: one-to-one sessions built on years of experience with clients of every age and starting point.",
                body, preload="lia-portrait")


def method():
    body = f"""
<section class="section method" aria-labelledby="method-title">
  <div class="container">
    <div class="section-intro">
      <div>
        <p class="eyebrow">The LIA method</p>
        <h1 id="method-title" class="h2"><span class="line">Not a class.</span> <span class="line">Your session.</span></h1>
      </div>
      <p class="lead">Every session is planned around one person. What you work on depends on how you’re moving, how you feel and where you want to go.</p>
    </div>
    <ol class="steps">
      <li class="step"><span class="step__n">01</span> <h2>Observe</h2> <p>See how you move before changing anything.</p></li>
      <li class="step"><span class="step__n">02</span> <h2>Understand</h2> <p>Find where things feel restricted, weak or disconnected.</p></li>
      <li class="step"><span class="step__n">03</span> <h2>Move</h2> <p>Combine Pilates, mobility and neuromovement as needed.</p></li>
      <li class="step"><span class="step__n">04</span> <h2>Progress</h2> <p>Adapt the work as your body changes.</p></li>
    </ol>
    <p class="method__close"><span class="line">This isn’t a fixed programme.</span> <em class="line">It changes as you do.</em></p>
  </div>
</section>

<section class="section" aria-labelledby="first-title">
  <div class="container about__grid">
    <figure class="about__portrait">{img('pilates', style='aspect-ratio:4/5;object-position:42% 50%')}</figure>
    <div>
      <p class="eyebrow">Your first session</p>
      <h2 id="first-title" class="h2" style="margin-top:var(--space-4)">It starts with a conversation.</h2>
      <div class="prose" style="margin-top:var(--space-5)">
        <p>Before any exercise, Lia asks about your history, how you spend your days and what you’d like to change. Then she watches a few simple movements to see how you actually move.</p>
        <p>From there, the session takes shape: some Pilates for strength, some mobility where things feel tight, some neuromovement to sharpen balance and coordination. The mix changes as you do.</p>
      </div>
    </div>
  </div>
</section>
{next_list(heading="The three disciplines")}
{CLOSING}"""
    return page("/method/", "The Method — LIA Pilates, Mobility &amp; Neuromovement",
                "Observe, understand, move, progress: how each LIA session is planned around one person.",
                body)


def discipline(key):
    d = DISCIPLINES[key]
    include = "\n".join(f"          <li>{x}</li>" for x in d["include"])
    suits = "\n".join(f"          <li>{x}</li>" for x in d["suits"])
    prose = "\n".join(f"        <p>{x}</p>" for x in d["prose"])
    body = f"""
<section class="page-head" aria-labelledby="page-title">
  <div class="container">
    <p class="eyebrow">Discipline {d['num']}</p>
    <h1 id="page-title" class="h1">{d['name']}</h1>
    <p class="page-head__statement">{d['statement']}</p>
  </div>
</section>

<section class="section" style="padding-top:0" aria-label="{d['name']} in practice">
  <div class="container">
    <figure class="disc-media">{img(d['img'], style='object-position:' + d['pos'], priority=True)}</figure>
    <div class="disc-body">
      <div class="prose">
        <p class="lead" style="color:var(--ink)">{d['short']}</p>
{prose}
      </div>
      <aside class="disc-aside">
        <div>
          <h2>A session can include</h2>
          <ul>
{include}
          </ul>
        </div>
        <div>
          <h2>Often helpful for</h2>
          <ul>
{suits}
          </ul>
        </div>
        <a class="btn btn--primary" href="/contact/?interest={d['name']}">Enquire about {d['name'] if key == 'pilates' else d['name'].lower()}</a>
      </aside>
    </div>
  </div>
</section>
{next_list(exclude=key)}
{CLOSING}"""
    return page(f"/{key}/", f"{d['name']} — LIA Pilates, Mobility &amp; Neuromovement",
                f"{d['name']} with Lia in Jumeirah Park, Dubai. {d['short']}", body, preload=IMG[d['img']][0])


def studio():
    body = f"""
<section class="page-head" aria-labelledby="page-title">
  <div class="container">
    <p class="eyebrow">The studio</p>
    <h1 id="page-title" class="h1">A quieter way to train.</h1>
    <p class="lead">Private sessions in a calm home studio in Jumeirah Park, with the time and space to focus entirely on you.</p>
  </div>
</section>

<section class="section" style="padding-top:0" aria-label="About the space">
  <div class="container">
    <figure class="disc-media disc-media--wide">{img('studio', style='object-position:45% 50%', priority=True)}</figure>
    <div class="notes">
      <div class="note"><h2>Private setting</h2> <p>Sessions take place in Lia’s home in Jumeirah Park. The address is shared when you book.</p></div>
      <div class="note"><h2>One client at a time</h2> <p>No class next door and nobody waiting. The time is yours.</p></div>
      <div class="note"><h2>Equipped for the work</h2> <p>A reformer, mats and small equipment for mobility and balance, in a bright, quiet room.</p></div>
    </div>
  </div>
</section>
{CLOSING}"""
    return page("/studio/", "The Studio — LIA Pilates, Mobility &amp; Neuromovement",
                "A calm home studio in Jumeirah Park, Dubai: one client at a time, with a reformer and space to move.",
                body, preload="studio-wide")


def contact():
    body = """
<section class="section contact" aria-labelledby="contact-title">
  <div class="container contact__grid">
    <div class="contact__info">
      <p class="eyebrow">Book a session</p>
      <h1 id="contact-title" class="h2">Let’s begin with a conversation.</h1>
      <p class="lead">Tell Lia a little about yourself and what you’d like from your sessions. She’ll reply personally to arrange a time.</p>
      <dl class="details">
        <div class="details__row" data-contact="whatsapp" hidden><dt>WhatsApp</dt> <dd><a href="#" target="_blank" rel="noopener" data-value></a></dd></div>
        <div class="details__row" data-contact="phone" hidden><dt>Phone</dt> <dd><a href="#" data-value></a></dd></div>
        <div class="details__row" data-contact="email" hidden><dt>Email</dt> <dd><a href="#" data-value></a></dd></div>
        <div class="details__row" data-contact="instagram" hidden><dt>Instagram</dt> <dd><a href="#" target="_blank" rel="noopener" data-value></a></dd></div>
        <div class="details__row"><dt>Studio</dt> <dd><span class="line">Home studio</span> <span class="line">Jumeirah Park, Dubai</span></dd></div>
        <div class="details__row"><dt>Sessions</dt> <dd><span class="line">By appointment</span> <span class="line">One-to-one</span></dd></div>
      </dl>
    </div>

    <form class="form" name="booking" method="POST" action="/thank-you.html" data-netlify="true" netlify-honeypot="company" novalidate>
      <input type="hidden" name="form-name" value="booking">
      <div hidden aria-hidden="true"><input name="company" tabindex="-1" autocomplete="off"></div>
      <div class="form__row">
        <div class="field">
          <label for="f-name">Name</label>
          <input id="f-name" name="name" autocomplete="name" required aria-describedby="f-name-err">
          <p class="field__error" id="f-name-err" aria-live="polite"></p>
        </div>
        <div class="field">
          <label for="f-phone">Phone or WhatsApp <span>(optional)</span></label>
          <input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel">
        </div>
      </div>
      <div class="field">
        <label for="f-email">Email</label>
        <input id="f-email" name="email" type="email" autocomplete="email" required aria-describedby="f-email-err">
        <p class="field__error" id="f-email-err" aria-live="polite"></p>
      </div>
      <div class="field">
        <label for="f-interest">I’m interested in</label>
        <select id="f-interest" name="interest">
          <option>Not sure yet, I’d like advice</option>
          <option>Pilates</option>
          <option>Mobility</option>
          <option>Neuromovement</option>
          <option>A combination</option>
        </select>
      </div>
      <div class="field">
        <label for="f-msg">A little about you <span>(optional)</span></label>
        <textarea id="f-msg" name="message" placeholder="How you feel at the moment, what you’d like to change, and which days or times suit you."></textarea>
      </div>
      <div class="form__foot">
        <p>Your details are only used to reply to you.</p>
        <button class="btn btn--primary" type="submit">Send request</button>
      </div>
      <p class="form__status" role="status" hidden></p>
    </form>
  </div>
</section>"""
    return page("/contact/", "Book a Session — LIA Pilates, Mobility &amp; Neuromovement",
                "Book a one-to-one Pilates, mobility or neuromovement session with Lia in Jumeirah Park, Dubai.", body)


def not_found():
    body = """
<section class="page-head" aria-labelledby="page-title" style="padding-bottom:var(--section)">
  <div class="container">
    <p class="eyebrow">Page not found</p>
    <h1 id="page-title" class="h1">This page has moved.</h1>
    <p class="lead">The site has been reorganised into separate pages. Everything is still here.</p>
    <div class="hero__ctas"><a class="btn btn--primary" href="/">Go to the home page</a> <a class="btn btn--secondary" href="/contact/">Book a session</a></div>
  </div>
</section>"""
    return page("/404", "Page not found — LIA", "This page could not be found.", body)


def main():
    out = {
        "index.html": home(),
        "about/index.html": about(),
        "method/index.html": method(),
        "studio/index.html": studio(),
        "contact/index.html": contact(),
        "404.html": not_found(),
    }
    for key in DISCIPLINES:
        out[f"{key}/index.html"] = discipline(key)
    for rel, html in out.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html)
        print("wrote", rel)


if __name__ == "__main__":
    main()
