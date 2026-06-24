#!/usr/bin/env python3
"""Build Decker Tape inner pages from a shared shell.
Run: python3 build.py   (writes tape/printed-tape/labels/capabilities/about/contact .html)
index.html is hand-authored and not generated here."""
import pathlib

SITE = "https://www.deckertape.com"
OUT = pathlib.Path(__file__).parent

# DEMO MODE: keep this True while the site is hosted on a temporary pitch domain so
# search engines never index the concept and it can't be confused with the real
# deckertape.com. Set to False (and re-run build.py) only when launching on the real domain.
DEMO_NOINDEX = True
ROBOTS_META = '\n<meta name="robots" content="noindex, nofollow">' if DEMO_NOINDEX else ""

NAV = [
    ("tape.html", "Tape"),
    ("printed-tape.html", "Printed Tape"),
    ("labels.html", "Labels"),
    ("catalog.html", "Catalog"),
    ("capabilities.html", "Capabilities"),
    ("about.html", "About"),
    ("contact.html", "Contact"),
]


def head(title, desc, slug, jsonld, keywords):
    canonical = f"{SITE}/{slug}"
    blocks = "\n".join(
        '<script type="application/ld+json">\n%s\n</script>' % j for j in jsonld
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">{ROBOTS_META}
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#262223">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Decker Tape Products">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/images/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<link rel="icon" href="images/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo+Expanded:wght@700;800&family=IBM+Plex+Mono:wght@500;600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
{blocks}
</head>
<body>
"""


def header(active):
    links = "\n".join(
        '      <li><a href="{href}"{cur}>{label}</a></li>'.format(
            href=h, label=l, cur=' aria-current="page"' if h == active else ""
        )
        for h, l in NAV
    )
    mobile = "\n".join(f'  <a href="{h}">{l}</a>' for h, l in NAV)
    return f"""<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="index.html" aria-label="Decker Tape Products — home">
      <img src="images/decker-logo.svg" alt="Decker Tape Products" width="170" height="34">
    </a>
    <ul class="nav-links">
{links}
    </ul>
    <div class="nav-cta">
      <a class="nav-phone" href="tel:18002275252">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        (800) 227-5252
      </a>
      <a class="btn" href="contact.html">Get a Quote <span class="arr">→</span></a>
    </div>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
  </div>
</header>
<nav class="mobile-panel" aria-label="Mobile">
{mobile}
  <a class="btn" href="contact.html">Get a Quote →</a>
  <p class="mobile-phone">(800) 227-5252 · info@deckertape.com</p>
</nav>
"""


def page_hero(crumb_label, eyebrow, h1, lede):
    return f"""<section class="page-hero">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a> <span class="sep">/</span> {crumb_label}</p>
    <span class="eyebrow eyebrow--light" style="margin-top:1.1rem;display:inline-flex;">{eyebrow}</span>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>
"""


CTA = """<section class="section">
  <div class="wrap">
    <div class="cta-band reveal">
      <div>
        <h2>Tell us your spec. We'll solve it.</h2>
        <p>Widths, colors, adhesives, quantities — send us what you need and our team will come back with a tailored solution and a quote.</p>
      </div>
      <div class="cta-band__actions">
        <a class="btn btn--white btn--lg" href="contact.html">Request a quote <span class="arr">→</span></a>
        <a class="btn btn--ghost-light btn--lg" href="tel:18002275252">(800) 227-5252</a>
      </div>
    </div>
  </div>
</section>
"""

FOOTER = """<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        <img src="images/decker-logo.svg" alt="Decker Tape Products" width="180" height="38">
        <p>Your total tape solution since 1969. Pressure-sensitive tape, custom printed tape, and labels — manufactured and converted in East Hanover, New Jersey.</p>
        <div class="socials">
          <a href="https://www.facebook.com/profile.php?id=61564830662560" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 12a10 10 0 1 0-11.5 9.9v-7H8v-2.9h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.2c-1.2 0-1.6.8-1.6 1.6V12H16l-.4 2.9h-2.1v7A10 10 0 0 0 22 12z"/></svg></a>
          <a href="https://twitter.com/decker_tape" aria-label="X / Twitter"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.9 2H22l-7.4 8.5L23 22h-6.8l-5.3-7-6.1 7H1.7l7.9-9L1 2h7l4.8 6.4L18.9 2zm-2.4 18h1.9L7.6 4H5.6l10.9 16z"/></svg></a>
          <a href="https://www.instagram.com/deckertape1969/" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg></a>
          <a href="https://www.linkedin.com/company/decker-tape-products/" aria-label="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.94 5a2 2 0 1 1-4 0 2 2 0 0 1 4 0zM3 8.5h3.9V21H3V8.5zm6.5 0h3.7v1.7h.1c.5-1 1.8-2 3.6-2 3.9 0 4.6 2.5 4.6 5.8V21h-3.9v-5.6c0-1.3 0-3-1.9-3s-2.1 1.4-2.1 2.9V21H9.5V8.5z"/></svg></a>
        </div>
      </div>
      <div class="footer-col">
        <h4>Products</h4>
        <ul>
          <li><a href="tape.html">Tape</a></li>
          <li><a href="printed-tape.html">Printed Tape</a></li>
          <li><a href="labels.html">Labels</a></li>
          <li><a href="catalog.html">Full Catalog</a></li>
          <li><a href="capabilities.html">Capabilities</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <ul>
          <li><a href="about.html">About Us</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="contact.html">Request a Quote</a></li>
          <li><a href="shipping.html">Shipping</a></li>
          <li><a href="returns.html">Returns</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Get in touch</h4>
        <ul>
          <li><a href="tel:18002275252">(800) 227-5252</a></li>
          <li><a href="mailto:info@deckertape.com">info@deckertape.com</a></li>
          <li>906C Murray Road<br>East Hanover, NJ 07936</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span id="year">2025</span> Decker Tape Products, Inc. All rights reserved.</span>
      <span>Your Total Tape Solution</span>
    </div>
  </div>
</footer>
<script src="main.js"></script>
</body>
</html>
"""


def breadcrumb_ld(label, slug):
    return (
        '{\n"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[\n'
        '{"@type":"ListItem","position":1,"name":"Home","item":"%s/"},\n'
        '{"@type":"ListItem","position":2,"name":"%s","item":"%s/%s"}]\n}'
        % (SITE, label, SITE, slug)
    )


def write(slug, html):
    (OUT / slug).write_text(html, encoding="utf-8")
    print("wrote", slug)


# ---- shared small icon set ----
IC = {
    "box": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 8 12 3 3 8v8l9 5 9-5V8z"/><path d="M3 8l9 5 9-5M12 13v8"/></svg>',
    "layers": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2 2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5"/></svg>',
    "wave": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12c2-3 4-3 6 0s4 3 6 0 4-3 6 0"/><path d="M2 17c2-3 4-3 6 0s4 3 6 0 4-3 6 0"/></svg>',
    "brush": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11V4a2 2 0 0 1 4 0v7"/><rect x="5" y="11" width="14" height="4" rx="1"/><path d="M7 15v3a3 3 0 0 0 6 0M9 21h2"/></svg>',
    "film": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 4v16M17 4v16M3 9h4M3 15h4M17 9h4M17 15h4"/></svg>',
    "star": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3l2.9 5.9 6.5.9-4.7 4.6 1.1 6.5L12 18l-5.8 3 1.1-6.5L2.6 9.8l6.5-.9L12 3z"/></svg>',
    "print": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="6" y="3" width="12" height="6" rx="1"/><path d="M6 14h12M6 9h12a2 2 0 0 1 2 2v7H4v-7a2 2 0 0 1 2-2z"/><rect x="8" y="16" width="8" height="5"/></svg>',
    "handle": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 11V8a5 5 0 0 1 10 0v3"/><rect x="4" y="11" width="16" height="9" rx="2"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>',
    "tag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 12 12 20l-8-8V4h8z"/><circle cx="8" cy="8" r="1.5"/></svg>',
    "scissors": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.12 15.88M14.47 14.48 20 20M8.12 8.12 12 12"/></svg>',
    "roll": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3"/></svg>',
    "grid": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>',
    "gear": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.6a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    "bulb": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18h6M10 22h4M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.1V18h6v-1.2c0-.8.4-1.6 1-2.1A7 7 0 0 0 12 2z"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="M22 4 12 14.01l-3-3"/></svg>',
    "hands": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 14 7 10a2 2 0 0 0-3 3l5 5 6-2 5-5a2 2 0 0 0-3-3l-3 3"/><path d="M11 14l2-2"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 12-9 12s-9-5-9-12a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
}


def card(icon, h3, p, spec=None):
    s = f'<span class="card-spec">{spec}</span>' if spec else ""
    return f"""      <article class="feat-card reveal">
        <span class="ico">{icon}</span>
        <h3>{h3}</h3>
        <p>{p}</p>
        {s}
      </article>"""


def spec_table(rows, cols=("Specification", "Typical range")):
    body = "\n".join(
        f'        <tr><td>{a}</td><td class="mono">{b}</td></tr>' for a, b in rows
    )
    return f"""      <table class="spec-table">
        <thead><tr><th>{cols[0]}</th><th>{cols[1]}</th></tr></thead>
        <tbody>
{body}
        </tbody>
      </table>"""


# =====================================================================
# TAPE
# =====================================================================
tape_ld = [
    breadcrumb_ld("Tape", "tape.html"),
    '{\n"@context":"https://schema.org","@type":"ProductGroup","name":"Pressure-Sensitive Tape","brand":{"@type":"Brand","name":"Decker Tape Products"},"description":"A broad range of pressure-sensitive tapes including carton sealing, double-sided, foam, masking, film and specialty tapes."\n}',
]
tape_cards = "\n".join([
    card(IC["box"], "Carton Sealing — BOPP", "BOPP carton-sealing tape with acrylic, hot-melt rubber or natural-rubber adhesive for case sealing, bundling and bulk packs.", "146 · 147 · 150 · 155"),
    card(IC["film"], "Crystal-Clear &amp; Premium Film", "Crystal-clear BOPP for clean, high-clarity seals and label protection — UV-resistant and won't yellow.", "120 · 123"),
    card(IC["wave"], "Bag Sealing", "UPVC bag-sealing tape with natural-rubber adhesive — high tack, 12 colors, approved for indirect food contact.", "125"),
    card(IC["layers"], "Double-Coated &amp; Foam", "Double-coated film, tissue and PE-foam tapes for mounting, splicing, laminating and gasketing.", "418A · 426L · 466"),
    card(IC["brush"], "Masking &amp; Paper", "Crepe masking, high-temperature masking and protective paper tapes for paint, powder-coat and surface protection.", "1222 · 275 · 278"),
    card(IC["star"], "Specialty &amp; High-Temp", "PTFE / glass cloth, splicing, security-cut, spooled and return tapes — engineered when off-the-shelf won't do.", "520 · 525 · 100ST"),
])
tape = (
    head(
        "Pressure-Sensitive Tape, Carton Sealing & More | Decker",
        "BOPP carton-sealing, crystal-clear, bag-sealing, foam, masking and specialty pressure-sensitive tape from Decker Tape — standard stock or built to your spec.",
        "tape.html", tape_ld,
        "pressure sensitive tape, carton sealing tape, double sided tape, foam tape, masking tape, polypropylene film tape, specialty tape, tape manufacturer NJ",
    )
    + header("tape.html")
    + page_hero("Tape", "Products / Tape",
               "Pressure-sensitive tape, held&nbsp;to one standard.",
               "Packaging, bonding, mounting, masking — a broad range of pressure-sensitive tapes, in standard stock or built to your exact construction. The same high quality runs through every roll we ship.")
    + """<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">The range</span>
      <h2>Tape for the job in front of you</h2>
      <p class="lede">Tell us the surface, the conditions, and the adhesive performance you need. We'll point you to the right construction — or make one.</p>
    </div>
    <div class="card-grid">
"""
    + tape_cards
    + """
    </div>
  </div>
</section>

<section class="section section--concrete">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Real spec sheets</span><h2>Representative constructions</h2>
    <p class="lede">Technical data taken directly from Decker spec sheets. Hundreds more constructions, widths and colors are available — full sheets on request.</p></div>
    <div class="reveal" style="overflow-x:auto;">
      <table class="spec-table">
        <thead><tr><th>Product</th><th>Backing</th><th>Adhesive</th><th>Thickness</th><th>Service temp</th></tr></thead>
        <tbody>
          <tr><td>150X — Carton sealing</td><td>BOPP</td><td class="mono">Acrylic</td><td class="mono">2.0 mil</td><td class="mono">25–104°F</td></tr>
          <tr><td>120 — Crystal clear</td><td>BOPP</td><td class="mono">Solvent acrylic</td><td class="mono">2.0 mil</td><td class="mono">−4–122°F</td></tr>
          <tr><td>125 — Bag sealing</td><td>UPVC</td><td class="mono">Natural rubber</td><td class="mono">2.3 mil</td><td class="mono">−4–158°F</td></tr>
          <tr><td>418A — Double-coated foam</td><td>PE foam</td><td class="mono">—</td><td class="mono">1/8&quot;</td><td class="mono">—</td></tr>
        </tbody>
      </table>
    </div>
    <p style="margin-top:2rem;"><a class="btn btn--ghost" href="catalog.html">Browse the full tape catalog <span class="arr">→</span></a></p>
  </div>
</section>
"""
    + CTA + FOOTER
)
write("tape.html", tape)

# =====================================================================
# PRINTED TAPE
# =====================================================================
pt_ld = [
    breadcrumb_ld("Printed Tape", "printed-tape.html"),
    '{\n"@context":"https://schema.org","@type":"Product","name":"Custom & Stock Printed Tape","brand":{"@type":"Brand","name":"Decker Tape Products"},"description":"Custom-printed and stock-printed pressure-sensitive tape, plus tape handles and pads. Decker is the only US manufacturer of pre-laminated tape handles.","category":"Printed Packaging Tape"\n}',
]
pt_cards = "\n".join([
    card(IC["print"], "Custom Printed Tape", "Your logo or message printed on pressure-sensitive carton-sealing tape — turn every sealed box into a billboard.", "100CP · 147XCP · 150CP"),
    card(IC["shield"], "Stock Printed Messages", "Ready-to-run printed messages on 1.83-mil BOPP — Fragile, Caution, Packing List Enclosed and dozens more.", "150SP series"),
    card(IC["handle"], "Tape Handles", "Pre-laminated handles let customers carry heavy cases with ease. Decker is the only US company that makes them.", "1575 · 1595 · 1325C"),
    card(IC["grid"], "Tape Pads", "Tear-away tape pads for retail, agricultural and warehouse use — great for repairing bags of mulch, seed and feed.", "1322 · 1404 · 1930"),
])
pt = (
    head(
        "Custom & Stock Printed Tape, Handles & Pads | Decker",
        "Custom-printed and stock-printed pressure-sensitive tape, plus tape handles and pads — Decker is the only US maker of pre-laminated tape handles.",
        "printed-tape.html", pt_ld,
        "custom printed tape, printed packaging tape, branded tape, stock printed tape, tape handles, pre-laminated tape handles, tape pads, Decker Tape",
    )
    + header("printed-tape.html")
    + page_hero("Printed Tape", "Products / Printed Tape",
               "Custom printed tape that ships your&nbsp;brand.",
               "Every sealed carton is a billboard. Put your logo or message directly on the tape — or pick from dozens of stock-printed messages. Plus tape handles and pads, including the pre-laminated handles only Decker makes in the US.")
    + """<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">What we print</span><h2>More than a seal</h2>
    <p class="lede">Printed tape turns a commodity into a touchpoint — the first thing your customer sees, and a job your packaging can do for free.</p></div>
    <div class="card-grid">
"""
    + pt_cards
    + """
    </div>
  </div>
</section>

<section class="section section--concrete">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Stock printed messages</span><h2>Off-the-shelf, ready to run</h2>
    <p class="lede">A selection of Decker's stock-printed messages, printed on 1.83-mil BOPP carton-sealing tape — no plate charge, no waiting.</p></div>
    <div class="chips chips--mono reveal">
      <span class="tag">Fragile</span><span class="tag">Caution!</span><span class="tag">Packing List Enclosed</span><span class="tag">If Seal Is Broken</span><span class="tag">Do Not Double Stack</span><span class="tag">Do Not Break Down Pallet</span><span class="tag">Mixed Merchandise Enclosed</span><span class="tag">Rush</span><span class="tag">Inspected</span><span class="tag">Repack</span><span class="tag">Opened for Customs Purposes</span><span class="tag">Warning</span><span class="tag">Season's Greetings</span>
    </div>
  </div>
</section>

<section class="section section--dark">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow eyebrow--light">How it runs</span><h2>From artwork to roll</h2>
    <p class="lede">A straightforward path from your logo to printed tape on your dock.</p></div>
    <div class="process">
      <div class="step reveal"><h3>Artwork</h3><p>Send your logo or message. We prep print-ready art and recommend colors.</p></div>
      <div class="step reveal"><h3>Proof</h3><p>You approve a proof for color, placement and repeat before we run.</p></div>
      <div class="step reveal"><h3>Print</h3><p>We print your custom or stock design on pressure-sensitive tape on our own presses.</p></div>
      <div class="step reveal"><h3>Convert</h3><p>Slit, spooled, padded or made into handles — finished to your spec.</p></div>
    </div>
  </div>
</section>
"""
    + CTA + FOOTER
)
write("printed-tape.html", pt)

# =====================================================================
# LABELS
# =====================================================================
lb_ld = [
    breadcrumb_ld("Labels", "labels.html"),
    '{\n"@context":"https://schema.org","@type":"ProductGroup","name":"Labels","brand":{"@type":"Brand","name":"Decker Tape Products"},"description":"Stock and custom printed labels, die-cut to shape and supplied on rolls or sheets."\n}',
]
lb_cards = "\n".join([
    card(IC["shield"], "Special Handling", "Fragile, This Side Up, Handle With Care, Glass and Do-Not-Stack labels that keep shipments intact.", "DL series"),
    card(IC["box"], "Regulated &amp; D.O.T.", "D.O.T., regulated, hazard and hazardous-communication labels for compliant shipping.", "regulated · hazmat"),
    card(IC["star"], "International Pictograph", "Wordless international handling symbols that cross any language barrier on the dock.", "international wordless"),
    card(IC["tag"], "Color Coded &amp; Inventory", "Color-coded dots, inventory, control, production / quality, numbers and month labels for the floor.", "color · inventory"),
    card(IC["scissors"], "Arrows, Circles &amp; Fluorescent", "Arrow labels, 1\\\"–4\\\" circles and high-visibility fluorescent labels in stock.", "1\\\"–4\\\" circles"),
    card(IC["print"], "Custom Printed Labels", "Your art and copy, die-cut to shape and supplied on rolls or sheets for your line.", "custom die-cut"),
])
lb = (
    head(
        "Shipping & Handling Labels, Custom & Die-Cut | Decker",
        "Special-handling, D.O.T., regulated, pictograph and custom die-cut labels from Decker Tape — on rolls or sheets, ready for your line and your brand.",
        "labels.html", lb_ld,
        "custom labels, printed labels, die cut labels, roll labels, stock labels, label manufacturer NJ, product labels",
    )
    + header("labels.html")
    + page_hero("Labels", "Products / Labels",
               "Stock &amp; custom labels, die-cut to&nbsp;spec.",
               "From blank stock to fully custom printed and die-cut, our label department supplies labels on rolls or sheets — ready for your application, your line, and your brand.")
    + """<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Label options</span><h2>Labelled, your way</h2>
    <p class="lede">Material, adhesive, shape, finish and format — specify what you need and we'll supply it print-ready.</p></div>
    <div class="card-grid">
"""
    + lb_cards
    + """
    </div>
  </div>
</section>

<section class="section section--concrete">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Stock sizes</span><h2>Common label sizes, in stock</h2>
    <p class="lede">A sample of stock sizes across the special-handling range — custom sizes and shapes are die-cut to your spec.</p></div>
    <div class="chips chips--mono reveal">
      <span class="tag">2&quot; × 3&quot;</span><span class="tag">2½&quot; × 2½&quot;</span><span class="tag">3&quot; × 3&quot;</span><span class="tag">3&quot; × 5&quot;</span><span class="tag">4&quot; × 4&quot;</span><span class="tag">4&quot; × 6&quot;</span><span class="tag">2½&quot; × 7&quot;</span><span class="tag">1&quot; circle</span><span class="tag">2&quot; circle</span><span class="tag">3&quot; circle</span><span class="tag">4&quot; circle</span>
    </div>
    <p style="margin-top:2rem;"><a class="btn btn--ghost" href="catalog.html">Browse the full label catalog <span class="arr">→</span></a></p>
  </div>
</section>
"""
    + CTA + FOOTER
)
write("labels.html", lb)

# =====================================================================
# CAPABILITIES
# =====================================================================
cap_ld = [breadcrumb_ld("Capabilities", "capabilities.html")]
cap_items = [
    (IC["print"], "Tape Printing", "Custom and stock printing on pressure-sensitive tape with your messaging and brand art.", "custom &amp; stock"),
    (IC["scissors"], "Rewind Slitting", "Narrow and wide-web rewind slitting — razor, score and lathe — to precise widths.", "razor · score · lathe"),
    (IC["roll"], "Spooling", "Precision spooling of narrow-width tapes for automated, high-volume lines.", "narrow-width"),
    (IC["grid"], "Sheeting", "Tapes and adhesives cut to sheets and pads for flat-pack and kitting.", "sheets & pads"),
    (IC["layers"], "Laminating", "Multi-layer laminating, including the pre-laminated tape handles we uniquely produce.", "pre-laminated"),
    (IC["tag"], "Die-Cutting", "Custom die-cut shapes for labels, gaskets and application-specific parts.", "custom shapes"),
    (IC["box"], "Padding", "Padding of sheets into convenient, tear-away tape pads for the shop floor.", "tear-away pads"),
    (IC["gear"], "Custom Machinery", "When the spec doesn't exist yet, we design and build the machine that makes it.", "engineered in-house"),
]
cap_cards = "\n".join(
    f"""      <div class="cap reveal">
        <svg class="cap__ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{icon[icon.find('>')+1:icon.rfind('</svg>')]}</svg>
        <h3>{h3}</h3>
        <p>{p}</p>
        <span class="cap__spec">{spec}</span>
      </div>"""
    for icon, h3, p, spec in cap_items
)
cap = (
    head(
        "Tape Converting — Printing, Slitting & Spooling | Decker",
        "Decker Tape's converting: printing, rewind/razor/score/lathe slitting, spooling, sheeting, die-cutting and laminating — over 50 years of custom machinery.",
        "capabilities.html", cap_ld,
        "tape converting, rewind slitting, razor slitting, lathe slitting, tape spooling, sheeting, laminating, die cutting, custom tape manufacturing",
    )
    + header("capabilities.html")
    + page_hero("Capabilities", "Capabilities",
               "Your problem, our&nbsp;solution.",
               "Printing, rewind slit, razor slit, score slit, lathe slit, spooling, sheeting — you name it. Over the past 50 years we've designed and customized our own machinery, so when it comes to tape and labels we can do almost anything.")
    + """<section class="section section--dark">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow eyebrow--light">The converting floor</span><h2>What we can do</h2>
    <p class="lede">Eight core capabilities — plus the willingness to engineer a ninth when your spec demands it.</p></div>
    <div class="cap-grid">
"""
    + cap_cards
    + """
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Engineered in-house</span>
      <h2>When the machine doesn't exist, we build it.</h2>
      <p class="lede" style="margin-top:1rem;">Decker regularly designs and customizes machinery to meet demands the market can't supply off the shelf. That in-house engineering is why we can take on the constructions, widths and finishes other converters turn away.</p>
      <ul class="feature-list">
        <li><svg class="ck" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M20 6 9 17l-5-5"/></svg><span>Custom widths and tolerances down to the spec sheet.</span></li>
        <li><svg class="ck" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M20 6 9 17l-5-5"/></svg><span>Short runs and large production volumes alike.</span></li>
        <li><svg class="ck" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M20 6 9 17l-5-5"/></svg><span>Application expertise to match product to problem.</span></li>
      </ul>
      <a class="btn" href="contact.html" style="margin-top:1.8rem;">Bring us your spec <span class="arr">→</span></a>
    </div>
    <div class="split__media reveal">
      <svg viewBox="0 0 240 200" fill="none">
        <g stroke="#D1242B" stroke-width="2" fill="none"><circle cx="120" cy="100" r="78"/><circle cx="120" cy="100" r="58"/><circle cx="120" cy="100" r="38"/></g>
        <circle cx="120" cy="100" r="20" fill="#1a1718"/>
        <path d="M198 100 q22 4 34 20 q-20 7 -38 -2 z" fill="#D1242B"/>
      </svg>
    </div>
  </div>
</section>
"""
    + CTA + FOOTER
)
write("capabilities.html", cap)

# =====================================================================
# ABOUT
# =====================================================================
about_ld = [
    breadcrumb_ld("About", "about.html"),
    '{\n"@context":"https://schema.org","@type":"AboutPage","name":"About Decker Tape Products","description":"Established in 1969 by George Decker, Decker Tape Products has grown from a single machine in a garage into a leading supplier of pressure-sensitive tapes and labels."\n}',
]
about = (
    head(
        "About Decker Tape — Tape Manufacturer Since 1969, NJ",
        "Established in 1969 by George Decker, Decker Tape has been your go-to partner for tape and labels for over 55 years — made in East Hanover, NJ. Read our story.",
        "about.html", about_ld,
        "about Decker Tape, tape manufacturer history, George Decker, pressure sensitive tape company, New Jersey tape manufacturer since 1969",
    )
    + header("about.html")
    + page_hero("About", "Our story",
               "Your total tape solution since&nbsp;1969.",
               "A unique blend of product, application expertise, and home-built innovation — that's what's made Decker a partner worth keeping for more than five decades.")
    + """<section class="section">
  <div class="wrap split">
    <div class="reveal prose">
      <span class="eyebrow">The beginning</span>
      <h2 style="margin:.8rem 0 1.2rem;">One machine. A garage. A lot of determination.</h2>
      <p><span class="drop">Established in 1969</span> by George Decker — in a garage, with one machine and a whole lot of determination — Decker Tape has since grown into a leading supplier of pressure-sensitive tapes and labels.</p>
      <p>That growth never changed the founding idea: tape is a problem-solving business. The right construction, slit to the right width, printed with the right message, delivered on time. Do that consistently and customers stay.</p>
      <p>Today, Decker is your go-to partner for all things tape and labels — pressure-sensitive tape, custom and stock printed tape, and a deep range of labels — and remains the only company in the US to manufacture pre-laminated tape handles. All from our home in East Hanover, New Jersey.</p>
    </div>
    <div class="split__media reveal" style="background:var(--ink);">
      <svg viewBox="0 0 240 200" fill="none">
        <g stroke="#D1242B" stroke-width="2" fill="none"><circle cx="120" cy="100" r="80"/><circle cx="120" cy="100" r="62"/><circle cx="120" cy="100" r="44"/></g>
        <circle cx="120" cy="100" r="26" fill="#1a1718"/>
        <text x="120" y="107" text-anchor="middle" font-family="'Archivo Expanded',sans-serif" font-weight="800" font-size="20" fill="#FEFDFD">'69</text>
      </svg>
    </div>
  </div>
</section>

<section class="section section--concrete">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Why Decker</span><h2>We don't just sell tape — we solve sticky situations.</h2></div>
    <div class="prose reveal" style="margin-top:1.5rem;">
      <p>For over 55 years, we've been leading the charge in delivering top-notch adhesive solutions that businesses trust. Whether you're shipping, sealing, or branding, we're here to help your operations run smoother and look better while they're at it.</p>
      <p>Our team geeks out over finding creative, practical solutions tailored to your business needs. We've got the expertise, the tools, and the hustle to make it happen.</p>
      <p>It's not just about what we do — it's how we do it. At Decker Tape Products, we believe in partnerships over transactions. So whether you need a precision die-cut solution, custom-branded packaging tape, or a reliable go-to for all your adhesive needs, we've got your back.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">What we stand on</span><h2>Why customers stay</h2></div>
    <div class="values">
      <div class="value reveal"><span class="ico">""" + IC["star"] + """</span><div><h3>Quality products</h3><p>A broad range held to the highest, most consistent standard — roll after roll.</p></div></div>
      <div class="value reveal"><span class="ico">""" + IC["bulb"] + """</span><div><h3>Innovative technology</h3><p>We design and customize our own machinery to meet demands the market can't.</p></div></div>
      <div class="value reveal"><span class="ico">""" + IC["gear"] + """</span><div><h3>Custom capability</h3><p>Standard or specialty, short run or high volume — engineered to your spec.</p></div></div>
      <div class="value reveal"><span class="ico">""" + IC["hands"] + """</span><div><h3>Flexibility</h3><p>Experience, products and innovation pointed at your unique demands.</p></div></div>
    </div>
  </div>
</section>
"""
    + CTA + FOOTER
)
write("about.html", about)

# =====================================================================
# CONTACT
# =====================================================================
contact_ld = [
    breadcrumb_ld("Contact", "contact.html"),
    '{\n"@context":"https://schema.org","@type":"ContactPage","name":"Contact Decker Tape Products","mainEntity":{"@type":"Organization","name":"Decker Tape Products, Inc.","telephone":"+1-800-227-5252","email":"info@deckertape.com","address":{"@type":"PostalAddress","streetAddress":"906C Murray Road","addressLocality":"East Hanover","addressRegion":"NJ","postalCode":"07936-2202","addressCountry":"US"}}\n}',
]
contact = (
    head(
        "Contact Decker Tape — Request a Quote | (800) 227-5252",
        "Contact Decker Tape Products in East Hanover, NJ. Call (800) 227-5252 or request a quote for pressure-sensitive tape, printed tape, handles and labels.",
        "contact.html", contact_ld,
        "contact Decker Tape, tape quote, custom tape quote, label quote, East Hanover NJ tape supplier, request a quote",
    )
    + header("contact.html")
    + page_hero("Contact", "Contact",
               "Let's solve your tape&nbsp;problem.",
               "Widths, colors, adhesives, quantities — tell us what you need and our team will come back with a tailored solution and a quote.")
    + """<section class="section">
  <div class="wrap contact-grid">
    <div class="reveal">
      <span class="eyebrow">Reach us</span>
      <h2 style="margin-top:.8rem;">Talk to a tape person.</h2>
      <div class="info-block">
        <div class="info-item"><span class="ico">""" + IC["phone"] + """</span><div><h4>Phone</h4><a href="tel:18002275252">(800) 227-5252</a></div></div>
        <div class="info-item"><span class="ico">""" + IC["mail"] + """</span><div><h4>Email</h4><a href="mailto:info@deckertape.com">info@deckertape.com</a></div></div>
        <div class="info-item"><span class="ico">""" + IC["pin"] + """</span><div><h4>Address</h4><p>906C Murray Road<br>East Hanover, NJ 07936-2202</p></div></div>
        <div class="info-item"><span class="ico">""" + IC["box"] + """</span><div><h4>Free shipping</h4><p>On qualifying orders of $99 or more</p></div></div>
      </div>
      <div class="map-embed">
        <iframe title="Decker Tape Products location map" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
          src="https://maps.google.com/maps?q=906C%20Murray%20Road%2C%20East%20Hanover%2C%20NJ%2007936&t=&z=14&ie=UTF8&iwloc=&output=embed"></iframe>
      </div>
    </div>

    <div class="reveal">
      <form class="form" data-quote action="https://api.web3forms.com/submit" method="POST" novalidate>
        <h3 style="font-family:var(--font-display);text-transform:uppercase;margin-bottom:1.3rem;">Request a quote</h3>
        <!-- Web3Forms config: paste your free access key from https://web3forms.com (no account needed). -->
        <input type="hidden" name="access_key" value="YOUR_WEB3FORMS_ACCESS_KEY">
        <input type="hidden" name="subject" value="New quote request — deckertape.com">
        <input type="hidden" name="from_name" value="Decker Tape website">
        <!-- honeypot: real people leave this empty -->
        <input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off" style="display:none" aria-hidden="true">
        <div class="field field--row">
          <div><label for="name">Name</label><input id="name" name="name" type="text" autocomplete="name" required></div>
          <div><label for="company">Company</label><input id="company" name="company" type="text" autocomplete="organization"></div>
        </div>
        <div class="field field--row">
          <div><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
          <div><label for="phone">Phone</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
        </div>
        <div class="field">
          <label for="interest">I'm interested in</label>
          <select id="interest" name="interest">
            <option>Tape</option>
            <option>Custom printed tape</option>
            <option>Tape handles &amp; pads</option>
            <option>Labels</option>
            <option>Custom converting</option>
            <option>Something else</option>
          </select>
        </div>
        <div class="field">
          <label for="message">Tell us your spec</label>
          <textarea id="message" name="message" placeholder="Widths, colors, adhesives, quantities, timeline…"></textarea>
        </div>
        <button class="btn" type="submit">Send request <span class="arr">→</span></button>
        <p class="form__note">Prefer to talk? Call <a href="tel:18002275252">(800) 227-5252</a>.</p>
        <div class="form__ok" role="status">Thanks — your request is in. A Decker rep will follow up shortly.</div>
        <div class="form__err" role="alert">Something went wrong sending that. Please call <a href="tel:18002275252">(800) 227-5252</a> or email <a href="mailto:info@deckertape.com">info@deckertape.com</a>.</div>
      </form>
    </div>
  </div>
</section>
"""
    + FOOTER
)
write("contact.html", contact)

# =====================================================================
# CATALOG  (client-side search over the full real product list)
# =====================================================================
catalog_ld = [breadcrumb_ld("Catalog", "catalog.html")]
catalog = (
    head(
        "Product Catalog — Tape, Printed Tape & Labels | Decker",
        "Browse Decker Tape's full catalog — 1,200+ pressure-sensitive tapes, printed tapes, handles, pads and labels. Search by name or part number.",
        "catalog.html", catalog_ld,
        "Decker Tape catalog, tape part numbers, label catalog, pressure sensitive tape list, printed tape products, tape handles, BOPP tape",
    )
    + header("catalog.html")
    + page_hero("Catalog", "Catalog",
               "The whole Decker catalog.",
               "Every product below is pulled straight from deckertape.com — 1,200+ tapes, printed tapes, handles, pads and labels. Search by name or part number, filter by line, then send us what you need for a quote.")
    + """<section class="section">
  <div class="wrap">
    <div class="catalog-controls reveal">
      <input id="cat-search" type="search" placeholder="Search by name or part number — e.g. 150X, fragile, BOPP, foam…" autocomplete="off" aria-label="Search products">
      <div class="catalog-filters" id="cat-filters" role="tablist"></div>
      <p class="catalog-count mono" id="cat-count" aria-live="polite">Loading catalog…</p>
    </div>
    <div class="catalog-grid" id="cat-grid"></div>
    <div class="center" style="margin-top:2.5rem;"><button class="btn btn--ghost" id="cat-more" hidden>Show more products</button></div>
    <p class="catalog-note mono">Product data pulled live from deckertape.com. Pricing and ordering are handled by Decker — <a href="contact.html">request a quote</a> or call <a href="tel:18002275252">(800) 227-5252</a>.</p>
  </div>
</section>
"""
    + CTA + FOOTER
)
write("catalog.html", catalog)

# =====================================================================
# INFO / POLICY PAGES  (verified real content from deckertape.com)
# =====================================================================
def simple_page(slug, crumb, eyebrow, h1, lede, title, desc, kw, body_html):
    return (
        head(title, desc, slug, [breadcrumb_ld(crumb, slug)], kw)
        + header(slug)
        + page_hero(crumb, eyebrow, h1, lede)
        + f"""<section class="section"><div class="wrap"><div class="prose reveal">{body_html}</div></div></section>"""
        + CTA + FOOTER
    )

write("shipping.html", simple_page(
    "shipping.html", "Shipping", "Policies", "Shipping &amp; free&nbsp;shipping",
    "Decker ships orders nationwide. Qualifying orders of $99 or more ship free.",
    "Shipping — Free Shipping on Orders $99+ | Decker Tape",
    "Decker Tape Products shipping policy: free shipping on qualifying orders of $99 or more. Contact us for shipping questions.",
    "Decker Tape shipping, free shipping tape, tape shipping policy",
    """<p><strong>Free shipping</strong> is available on qualifying orders. If the items in your order that qualify for free shipping total <strong>$99 or more, your order ships free</strong>.</p>
    <p>Look for the free-shipping logo on qualifying items throughout the catalog. For shipping questions, lead times, freight on large orders, or expedited service, call <a href="tel:18002275252">(800)&nbsp;227-5252</a> or email <a href="mailto:info@deckertape.com">info@deckertape.com</a>.</p>"""))

write("returns.html", simple_page(
    "returns.html", "Returns", "Policies", "Returns",
    "Need to return an item? Our customer-service team will help.",
    "Returns | Decker Tape Products",
    "Decker Tape Products returns: contact customer service for help returning an item.",
    "Decker Tape returns, return policy, tape returns",
    """<p><strong>How do I return an item?</strong></p>
    <p>Please contact customer service for more information on returning an item. Call <a href="tel:18002275252">(800)&nbsp;227-5252</a> or email <a href="mailto:info@deckertape.com">info@deckertape.com</a> and we'll take care of you. Thank you.</p>"""))

print("done.")
