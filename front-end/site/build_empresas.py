# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from partials import navbar, footer, html_shell, page_header
from icons import ICONS
from illustrations import company_mark, car_card_illustration

EMPRESAS = [
    ("Auto Show Veículos", "Concessionária multimarcas", "AS", "#3ebd52", True, "4.9", "128"),
    ("Palmas Motors", "Revendedora", "PM", "#3577d4", True, "4.7", "86"),
    ("Oficina do Zé", "Oficina mecânica", "OZ", "#e2a02f", False, "4.5", "52"),
    ("Seguros Capital", "Seguradora", "SC", "#e0483f", True, "4.8", "203"),
    ("TO Corretora de Seguros", "Corretora", "TC", "#1a3a5c", True, "4.6", "64"),
]

def company_card(nome, cat, initials, color, verificada, nota, avals):
    seal = '<span class="badge badge-green" style="margin-left:8px">{s}Selo</span>'.format(s=ICONS["shield-check"]) if verificada else ""
    return '''
    <a href="empresa-detalhes.html" class="card company-card">
      <div class="company-logo" style="background:#0a1626">{mark}</div>
      <div style="flex:1">
        <h4>{nome}{seal}</h4>
        <div class="cat">{cat} · Palmas-TO</div>
        <div class="flex items-center gap-8">
          <span class="flex items-center gap-8" style="color:var(--amber-500);font-weight:700;font-size:13px">{star} {nota}</span>
          <span class="small">({avals} avaliações)</span>
        </div>
      </div>
    </a>'''.format(mark=company_mark(initials, size=56, color=color), nome=nome, seal=seal, cat=cat,
                    star=ICONS["star"], nota=nota, avals=avals)

def build_empresas():
    header = page_header([("Início", "index.html"), ("Empresas", None)], "Empresas parceiras",
                          "Concessionárias, revendas, oficinas, seguradoras e corretoras verificadas")

    filters = '''
    <div class="tabs" style="margin-bottom:28px">
      <a href="#" class="active">Todas</a>
      <a href="#">Revendedoras</a>
      <a href="#">Concessionárias</a>
      <a href="#">Oficinas</a>
      <a href="#">Seguradoras</a>
      <a href="#">Corretoras</a>
    </div>'''

    cards = "".join([company_card(*e) for e in EMPRESAS])
    grid = '<div class="grid-2">{cards}</div>'.format(cards=cards)

    content = '<div class="container" style="padding:36px 0 80px">{filters}{grid}</div>'.format(filters=filters, grid=grid)
    body = navbar("") + header + content + footer()
    return html_shell("Empresas parceiras", body, "Encontre lojas, oficinas e seguradoras verificadas em Palmas-TO.")

def build_empresa_detalhes():
    header = page_header([("Início", "index.html"), ("Empresas", "empresas.html"), ("Auto Show Veículos", None)],
                          "Auto Show Veículos", "Concessionária multimarcas · Palmas-TO")

    top = '''
    <div class="card card-pad flex items-center justify-between" style="margin-bottom:28px">
      <div class="flex items-center gap-12">
        <div class="company-logo" style="width:70px;height:70px">{mark}</div>
        <div>
          <h3 style="margin-bottom:4px">Auto Show Veículos <span class="badge badge-green" style="margin-left:6px">{shield}Selo de confiança</span></h3>
          <p class="small" style="margin:0">{pin} Av. Teotônio Segurado, 1450 - Plano Diretor Sul, Palmas-TO</p>
        </div>
      </div>
      <div class="flex gap-12">
        <a href="#" class="btn btn-outline-dark">{phone}(63) 3212-4477</a>
        <a href="#" class="btn btn-primary">{whats}WhatsApp</a>
      </div>
    </div>'''.format(mark=company_mark("AS", size=70), shield=ICONS["shield-check"], pin=ICONS["pin"],
                      phone=ICONS["phone"], whats=ICONS["phone"])

    tabs = '''
    <div class="tabs">
      <a href="#" class="active">Veículos (24)</a>
      <a href="#">Serviços</a>
      <a href="#">Sobre</a>
      <a href="#">Avaliações (128)</a>
    </div>'''

    cards = "".join([related(i) for i in range(6)])
    grid = '<div class="vehicle-grid">{cards}</div>'.format(cards=cards)

    content = '<div class="container" style="padding:32px 0 80px">{top}{tabs}{grid}</div>'.format(top=top, tabs=tabs, grid=grid)
    body = navbar("") + header + content + footer()
    return html_shell("Auto Show Veículos", body, "Veículos e serviços da Auto Show Veículos em Palmas-TO.")

def related(seed):
    return '''
        <div class="card vehicle-card">
          <div class="vehicle-photo">{illus}<a href="#" class="fav">{heart}</a></div>
          <div class="vehicle-body">
            <div class="price">R$ {preco}.900</div>
            <h4>Veículo disponível #{n}</h4>
            <div class="vehicle-footer">
              <span class="seller">{pin}Palmas-TO</span>
              <a href="veiculo-detalhes.html" class="btn btn-outline-dark btn-sm">Ver detalhes</a>
            </div>
          </div>
        </div>'''.format(illus=car_card_illustration(seed), heart=ICONS["heart"], preco=90+seed*8, n=seed+1, pin=ICONS["pin"])

if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for fname, fn in [("empresas.html", build_empresas), ("empresa-detalhes.html", build_empresa_detalhes)]:
        out = fn()
        with open(os.path.join(base, fname), "w", encoding="utf-8") as f:
            f.write(out)
        print("wrote", fname, len(out))
