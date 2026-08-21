# -*- coding: utf-8 -*-
from icons import ICONS

def logo_svg():
    return '<svg viewBox="0 0 48 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 16l2.4-7A3 3 0 0 1 7.2 7h17a3 3 0 0 1 2.9 1.8L29 16"/><path d="M2 16h27v5.5a1.5 1.5 0 0 1-1.5 1.5h-1.7a1.5 1.5 0 0 1-1.5-1.5V20H6.7v1.5A1.5 1.5 0 0 1 5.2 23H3.5A1.5 1.5 0 0 1 2 21.5z"/><circle cx="9.5" cy="20.3" r="2"/><circle cx="21" cy="20.3" r="2"/></svg>'

def brand(dashboard=False):
    return '''<a href="{home}" class="brand">
      {logo}
      <span>
        <span class="brand-word">Auto<span>Palmas</span></span>
        <span class="brand-tag">Conectando você ao melhor negócio.</span>
      </span>
    </a>'''.format(home="index.html", logo=logo_svg())

NAV_ITEMS = [
    ("comprar", "Comprar", "catalogo.html"),
    ("vender", "Vender", "vendedor-veiculo-form.html"),
    ("servicos", "Serviços", "servicos.html"),
    ("como-funciona", "Como funciona", "index.html#como-funciona"),
    ("sobre", "Sobre nós", "sobre.html"),
]

def navbar(active=""):
    links = []
    for key, label, href in NAV_ITEMS:
        cls = "active" if key == active else ""
        links.append('<a href="{href}" class="{cls}">{label}</a>'.format(href=href, cls=cls, label=label))
    links_html = "\n      ".join(links)
    return '''<header class="navbar">
    <div class="container">
      {brand}
      <nav class="nav-links">
      {links}
      </nav>
      <div class="nav-actions">
        <a href="comprador-interesses.html" class="icon-btn" title="Favoritos" aria-label="Favoritos">{heart}</a>
        <a href="login.html" class="nav-link-plain">Entrar</a>
        <a href="cadastro.html" class="btn btn-primary btn-sm">Cadastrar</a>
        <button class="nav-burger" aria-label="Abrir menu">{listicon}</button>
      </div>
    </div>
  </header>'''.format(brand=brand(), links=links_html, heart=ICONS["heart"], listicon=ICONS["list"])

def footer():
    return '''<footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-about">
          {brand}
          <p>A plataforma automotiva completa de Palmas-TO e região. Mais confiança, mais serviços, melhores negócios.</p>
          <div class="social-row">
            <a href="#" aria-label="Instagram">{instagram}</a>
            <a href="#" aria-label="Facebook">{facebook}</a>
            <a href="#" aria-label="WhatsApp">{whatsapp}</a>
            <a href="#" aria-label="YouTube">{youtube}</a>
          </div>
        </div>
        <div>
          <h5>Navegação</h5>
          <ul>
            <li><a href="catalogo.html">Comprar</a></li>
            <li><a href="vendedor-veiculo-form.html">Vender</a></li>
            <li><a href="servicos.html">Serviços</a></li>
            <li><a href="index.html#como-funciona">Como funciona</a></li>
            <li><a href="sobre.html">Sobre nós</a></li>
          </ul>
        </div>
        <div>
          <h5>Serviços</h5>
          <ul>
            <li><a href="seguros.html">Cotar seguro</a></li>
            <li><a href="servicos.html">Financiamento</a></li>
            <li><a href="servicos.html">Despachante</a></li>
            <li><a href="servicos.html">Oficinas parceiras</a></li>
            <li><a href="servicos.html">Avaliação de veículos</a></li>
          </ul>
        </div>
        <div>
          <h5>Institucional</h5>
          <ul>
            <li><a href="sobre.html">Quem somos</a></li>
            <li><a href="#">Termos de uso</a></li>
            <li><a href="#">Política de privacidade</a></li>
            <li><a href="#">Perguntas frequentes</a></li>
            <li><a href="#">Fale conosco</a></li>
          </ul>
        </div>
        <div>
          <h5>Baixe nosso app</h5>
          <p style="font-size:13px;color:rgba(255,255,255,.55)">Tenha a melhor experiência na palma da sua mão.</p>
          <div class="store-badges">
            <span class="store-badge"><svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M3 3.5v17a1 1 0 0 0 1.5.87L20 12 4.5 2.6A1 1 0 0 0 3 3.5z"/></svg> Disponível no Google Play</span>
            <span class="store-badge"><svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M16.4 2c.1 1.1-.3 2.1-1 2.9-.7.8-1.8 1.4-2.8 1.3-.1-1 .4-2.1 1-2.8.8-.9 2-1.4 2.8-1.4zm3.8 16.8c-.5 1.1-.8 1.6-1.4 2.5-.9 1.4-2.2 3.1-3.8 3.1-1.4 0-1.8-.9-3.7-.9s-2.4.9-3.7.9c-1.6 0-2.8-1.5-3.7-2.9C1.7 18.6.9 14.9 2 12.3c.6-1.4 1.7-2.9 3.4-2.9 1.4 0 2.3.9 3.5.9 1.1 0 1.8-.9 3.7-.9 1.5 0 3 .8 4 2.1-3.6 2-3 7.1.6 8.3z"/></svg> Disponível na App Store</span>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© 2026 AutoPalmas. Todos os direitos reservados.</span>
        <span>Palmas · Tocantins</span>
      </div>
    </div>
  </footer>'''.format(brand=brand(), instagram=ICONS["instagram"], facebook=ICONS["facebook"], whatsapp=ICONS["whatsapp"], youtube=ICONS["youtube"])

def page_header(crumbs, title, subtitle=""):
    """crumbs: list of (label, href|None)"""
    parts = []
    for i, (label, href) in enumerate(crumbs):
        if href:
            parts.append('<a href="{}">{}</a>'.format(href, label))
        else:
            parts.append('<span>{}</span>'.format(label))
    crumb_html = ' <span style="opacity:.4">/</span> '.join(parts)
    sub_html = '<p>{}</p>'.format(subtitle) if subtitle else ""
    return '''<div class="page-header">
    <div class="container">
      <div class="breadcrumb">{crumb}</div>
      <h1>{title}</h1>
      {sub}
    </div>
  </div>'''.format(crumb=crumb_html, title=title, sub=sub_html)

# ------------------- Dashboard shell (vendedor / empresa / comprador / admin) -------------------

DASH_NAV = {
    "vendedor": [
        ("Painel", "grid", "vendedor-dashboard.html"),
        ("Meus veículos", "car", "vendedor-veiculos.html"),
        ("Novo anúncio", "plus", "vendedor-veiculo-form.html"),
        ("Leads recebidos", "users", "vendedor-leads.html"),
        ("Meu perfil", "user", "perfil.html"),
    ],
    "empresa": [
        ("Painel", "grid", "empresa-dashboard.html"),
        ("Dados da empresa", "building", "empresa-cadastro.html"),
        ("Veículos", "car", "vendedor-veiculos.html"),
        ("Serviços", "wrench", "servicos.html"),
        ("Leads recebidos", "users", "vendedor-leads.html"),
        ("Verificação / Selo", "shield-check", "empresa-verificacao.html"),
    ],
    "comprador": [
        ("Meus interesses", "heart", "comprador-interesses.html"),
        ("Minhas cotações", "umbrella", "comprador-cotacoes.html"),
        ("Minhas compras", "handshake", "comprador-compras.html"),
        ("Meu perfil", "user", "perfil.html"),
    ],
    "admin": [
        ("Painel", "grid", "admin-dashboard.html"),
        ("Moderação de anúncios", "doc-check", "admin-moderacao.html"),
        ("Verificação de empresas", "shield-check", "admin-empresas.html"),
        ("Usuários", "users", "admin-usuarios.html"),
        ("Vendas", "money", "admin-vendas.html"),
    ],
}

ROLE_LABEL = {
    "vendedor": ("Camila Rocha", "Vendedora particular"),
    "empresa": ("Auto Show Veículos", "Representante de empresa"),
    "comprador": ("Rafael Nunes", "Comprador"),
    "admin": ("Equipe AutoPalmas", "Administrador"),
}

def dash_sidebar(role, active_href):
    items = DASH_NAV[role]
    lis = []
    for label, icon, href in items:
        cls = "active" if href == active_href else ""
        lis.append('<a href="{href}" class="{cls}">{icon}<span>{label}</span></a>'.format(
            href=href, cls=cls, icon=ICONS[icon], label=label))
    name, role_label = ROLE_LABEL[role]
    initials = "".join([p[0] for p in name.split()[:2]]).upper()
    avatar = '<div style="width:36px;height:36px;border-radius:50%;background:var(--green-500);color:#06210c;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;">{}</div>'.format(initials)
    return '''<aside class="dash-sidebar">
      {brand}
      <div class="dash-nav-group">
        <div class="dash-nav-label">Menu</div>
        <div class="dash-nav">
          {items}
        </div>
      </div>
      <div class="dash-nav-group">
        <div class="dash-nav-label">Conta</div>
        <div class="dash-nav">
          <a href="index.html">{home_icon}<span>Ver site público</span></a>
          <a href="login.html">{logout_icon}<span>Sair</span></a>
        </div>
      </div>
      <div class="dash-user">
        {avatar}
        <div>
          <strong>{name}</strong>
          <span>{role_label}</span>
        </div>
      </div>
    </aside>'''.format(brand=brand(), items="\n          ".join(lis), avatar=avatar, name=name,
                        role_label=role_label, home_icon=ICONS["arrow-right"], logout_icon=ICONS["logout"])

def dash_topbar(title, subtitle="", actions=""):
    return '''<div class="dash-topbar">
        <div>
          <h1>{title}</h1>
          <p>{subtitle}</p>
        </div>
        <div class="flex gap-12 items-center">{actions}</div>
      </div>'''.format(title=title, subtitle=subtitle, actions=actions)

def dash_page(role, active_href, title, subtitle, content, actions=""):
    return '''<div class="dash-shell">
      {sidebar}
      <main class="dash-main">
        {topbar}
        <div class="dash-content">
          {content}
        </div>
      </main>
    </div>'''.format(sidebar=dash_sidebar(role, active_href),
                      topbar=dash_topbar(title, subtitle, actions),
                      content=content)

# ------------------- HTML shell -------------------

def html_shell(title, body, description=""):
    return '''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · AutoPalmas</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
{body}
<script src="assets/js/app.js"></script>
</body>
</html>'''.format(title=title, desc=description or title, body=body)
