# -*- coding: utf-8 -*-
# Ilustrações SVG originais (sem fotos de terceiros) — linguagem visual AutoPalmas

def _buildings(x0, y0, seed=1):
    """Gera um horizonte de prédios simples em silhueta."""
    import random
    rnd = random.Random(seed)
    out = []
    x = x0
    while x < x0 + 900:
        w = rnd.randint(34, 68)
        h = rnd.randint(50, 170)
        out.append('<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#0f2036" opacity="0.9"/>'.format(x=x, y=y0 - h, w=w, h=h))
        # janelas
        wx = x + 6
        while wx < x + w - 8:
            wy = y0 - h + 10
            while wy < y0 - 8:
                if rnd.random() > 0.45:
                    out.append('<rect x="{wx}" y="{wy}" width="4" height="6" fill="#f4c95d" opacity="{o}"/>'.format(wx=wx, wy=wy, o=round(rnd.uniform(.25,.7),2)))
                wy += 14
            wx += 11
        x += w + rnd.randint(6, 16)
    return "".join(out)


def hero_illustration():
    """Cena grande: skyline noturno + SUV estilizado, tom navy/verde — usada no hero da home."""
    buildings = _buildings(-40, 430, seed=7)
    return '''<svg viewBox="0 0 900 560" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ilustração de um SUV estacionado com o horizonte de Palmas ao fundo">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0a1626"/>
      <stop offset="0.55" stop-color="#122a45"/>
      <stop offset="1" stop-color="#173a5e"/>
    </linearGradient>
    <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#173a5e"/>
      <stop offset="1" stop-color="#0a1626"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#55d267" stop-opacity="0.55"/>
      <stop offset="1" stop-color="#55d267" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="carBody" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#aab3c2"/>
      <stop offset="1" stop-color="#6c7688"/>
    </linearGradient>
  </defs>

  <rect width="900" height="560" fill="url(#sky)"/>
  <circle cx="740" cy="90" r="46" fill="#f4c95d" opacity=".85"/>
  <circle cx="740" cy="90" r="80" fill="#f4c95d" opacity=".08"/>

  <g>{buildings}</g>
  <rect x="0" y="430" width="900" height="130" fill="url(#ground)"/>
  <rect x="0" y="430" width="900" height="4" fill="#2ea043" opacity=".5"/>

  <!-- reflexo -->
  <ellipse cx="430" cy="520" rx="330" ry="26" fill="#000" opacity=".25"/>
  <circle cx="430" cy="470" r="230" fill="url(#glow)"/>

  <!-- SUV estilizado -->
  <g transform="translate(120,300)">
    <path d="M0 150 C 10 110, 40 95, 90 92 L 130 60 C 145 46, 168 38, 200 38 L 430 38 C 468 38, 500 52, 522 80 L 560 120 C 590 126, 612 138, 620 150 L 620 178 L 0 178 Z" fill="url(#carBody)"/>
    <path d="M150 92 L 190 55 C 202 46, 218 40, 238 40 L 400 40 C 425 40, 448 50, 465 68 L 500 92 Z" fill="#0d1e33" opacity=".92"/>
    <path d="M215 92 L 245 58 L 320 58 L 320 92 Z" fill="#173a5e"/>
    <path d="M330 92 L 330 58 L 395 58 L 420 92 Z" fill="#173a5e"/>
    <rect x="0" y="150" width="620" height="10" fill="#0a1626"/>
    <circle cx="130" cy="182" r="46" fill="#0a1626"/>
    <circle cx="130" cy="182" r="24" fill="#3c4453"/>
    <circle cx="130" cy="182" r="8" fill="#0a1626"/>
    <circle cx="500" cy="182" r="46" fill="#0a1626"/>
    <circle cx="500" cy="182" r="24" fill="#3c4453"/>
    <circle cx="500" cy="182" r="8" fill="#0a1626"/>
    <!-- farol -->
    <path d="M0 120 L 40 108 L 46 140 L 4 150 Z" fill="#eaf8ec"/>
    <circle cx="18" cy="126" r="26" fill="url(#glow)"/>
    <!-- placa -->
    <rect x="240" y="150" width="120" height="26" rx="4" fill="#fff"/>
    <text x="300" y="168" font-family="Poppins, sans-serif" font-size="14" font-weight="700" fill="#0a1626" text-anchor="middle">PALMAS-TO</text>
    <!-- friso verde -->
    <path d="M40 108 L 560 118" stroke="#3ebd52" stroke-width="3" opacity=".7"/>
  </g>
</svg>'''.format(buildings=buildings)


def cta_skyline():
    buildings = _buildings(-20, 210, seed=3)
    return '''<svg viewBox="0 0 620 220" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
  <g opacity=".8">{buildings}</g>
</svg>'''.format(buildings=buildings)


_CARD_PALETTE = [
    ("#aab3c2", "#6c7688"),  # prata
    ("#3c4453", "#20242e"),  # grafite
    ("#7c8797", "#454e5c"),  # cinza
    ("#c8d0da", "#8b95a3"),  # branco perolizado
    ("#2ea043", "#155c2a"),  # verde (destaque)
    ("#1a3a5c", "#0d1e33"),  # azul marinho
]

def car_card_illustration(seed=0, bg="#eef1f6"):
    """Ilustração compacta de carro para thumbnails de cards (catálogo, dashboards)."""
    top, bottom = _CARD_PALETTE[seed % len(_CARD_PALETTE)]
    uid = "cc{}".format(seed)
    return '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ilustração de veículo à venda">
  <defs>
    <linearGradient id="bg{u}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#f6f8fb"/>
      <stop offset="1" stop-color="{bg}"/>
    </linearGradient>
    <linearGradient id="body{u}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{top}"/>
      <stop offset="1" stop-color="{bottom}"/>
    </linearGradient>
  </defs>
  <rect width="400" height="300" fill="url(#bg{u})"/>
  <ellipse cx="200" cy="235" rx="150" ry="14" fill="#0a1626" opacity=".08"/>
  <g transform="translate(58,95)">
    <path d="M0 90 C 6 62, 26 52, 56 50 L 80 30 C 90 20, 104 15, 124 15 L 250 15 C 274 15, 294 24, 308 42 L 328 66 C 348 70, 362 78, 368 90 L 368 108 L 0 108 Z" fill="url(#body{u})"/>
    <path d="M92 50 L 114 32 C 122 26, 132 22, 146 22 L 232 22 C 248 22, 262 28, 272 40 L 288 50 Z" fill="#0d1e33" opacity=".85"/>
    <path d="M132 50 L 148 34 L 190 34 L 190 50 Z" fill="#173a5e"/>
    <path d="M198 50 L 198 34 L 230 34 L 246 50 Z" fill="#173a5e"/>
    <rect x="0" y="90" width="368" height="7" fill="#0a1626"/>
    <circle cx="78" cy="110" r="27" fill="#0a1626"/>
    <circle cx="78" cy="110" r="13" fill="#4a5364"/>
    <circle cx="298" cy="110" r="27" fill="#0a1626"/>
    <circle cx="298" cy="110" r="13" fill="#4a5364"/>
    <rect x="150" y="90" width="70" height="16" rx="3" fill="#fff"/>
  </g>
</svg>'''.format(u=uid, bg=bg, top=top, bottom=bottom)


_AV_COLORS = ["#3ebd52", "#1a3a5c", "#e2a02f", "#3577d4", "#e0483f", "#2ea043"]

def avatar(name, size=64, seed=None):
    initials = "".join([p[0].upper() for p in name.split()[:2]])
    color = _AV_COLORS[(seed if seed is not None else len(name)) % len(_AV_COLORS)]
    fs = int(size * 0.36)
    return '''<svg viewBox="0 0 {s} {s}" width="{s}" height="{s}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Avatar de {name}">
  <circle cx="{h}" cy="{h}" r="{h}" fill="{color}"/>
  <text x="{h}" y="{ty}" font-family="Poppins, sans-serif" font-size="{fs}" font-weight="600" fill="#ffffff" text-anchor="middle">{initials}</text>
</svg>'''.format(s=size, h=size/2, ty=size/2 + fs*0.34, fs=fs, color=color, initials=initials, name=name)


def company_mark(initials, size=56, color="#3ebd52"):
    fs = int(size * 0.36)
    return '''<svg viewBox="0 0 {s} {s}" width="{s}" height="{s}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Logo da empresa">
  <rect width="{s}" height="{s}" rx="{r}" fill="#0a1626"/>
  <text x="{h}" y="{ty}" font-family="Poppins, sans-serif" font-size="{fs}" font-weight="700" fill="{color}" text-anchor="middle">{initials}</text>
</svg>'''.format(s=size, r=size*0.22, h=size/2, ty=size/2 + fs*0.34, fs=fs, color=color, initials=initials)
