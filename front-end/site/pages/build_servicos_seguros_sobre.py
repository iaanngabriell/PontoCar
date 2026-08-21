# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from partials import navbar, footer, html_shell, page_header
from icons import ICONS
from illustrations import avatar, cta_skyline

SERVICOS = [
    ("wrench", "Oficinas parceiras", "Manutenção preventiva e corretiva com desconto exclusivo para usuários AutoPalmas."),
    ("doc-check", "Despachante", "Transferência, licenciamento e regularização de documentos sem sair de casa."),
    ("money", "Financiamento", "Simule e contrate financiamento com os principais bancos parceiros."),
    ("shield-check", "Avaliação de veículos", "Laudo cautelar e avaliação profissional antes de fechar negócio."),
    ("umbrella", "Seguro auto", "Cotação de seguro em poucos minutos com as maiores seguradoras do país."),
    ("car", "Guincho 24h", "Assistência e reboque em qualquer ponto de Palmas-TO e região."),
]

def build_servicos():
    header = page_header([("Início", "index.html"), ("Serviços", None)], "Serviços integrados",
                          "Tudo que você precisa para comprar, vender e cuidar do seu veículo")

    cards = ""
    for icon, titulo, desc in SERVICOS:
        cards += '''
        <div class="card card-pad">
          <div class="feature-icon" style="margin:0 0 16px">{icon}</div>
          <h4>{titulo}</h4>
          <p style="margin-bottom:16px">{desc}</p>
          <a href="#" class="btn btn-outline-dark btn-sm">Solicitar{arrow}</a>
        </div>'''.format(icon=ICONS[icon], titulo=titulo, desc=desc, arrow=ICONS["arrow-right"])

    grid = '<div class="grid-3">{cards}</div>'.format(cards=cards)
    content = '<div class="container" style="padding:36px 0 80px">{grid}</div>'.format(grid=grid)
    body = navbar("servicos") + header + content + footer()
    return html_shell("Serviços", body, "Financiamento, seguro, despachante, avaliação e oficinas parceiras em Palmas-TO.")


PLANOS = [
    ("Essencial", "R$ 89", "/mês", ["Cobertura contra roubo e furto", "Assistência 24h básica", "Carro reserva por 7 dias"], False),
    ("Completo", "R$ 149", "/mês", ["Cobertura total (colisão, roubo, incêndio)", "Assistência 24h completa", "Carro reserva por 15 dias", "Vidros e faróis inclusos"], True),
    ("Premium", "R$ 219", "/mês", ["Cobertura total + terceiros ampliada", "Assistência 24h premium", "Carro reserva por 30 dias", "Vidros, faróis e pequenos reparos"], False),
]

def build_seguros():
    header = page_header([("Início", "index.html"), ("Seguros", None)], "Cote seu seguro auto",
                          "Compare planos e contrate com as maiores seguradoras parceiras")

    form = '''
    <div class="form-card" style="margin-bottom:48px">
      <h3 style="margin-bottom:20px">Simular cotação</h3>
      <div class="form-row cols-3">
        <div class="form-group"><label>Marca</label><select class="form-control"><option>Selecione a marca</option></select></div>
        <div class="form-group"><label>Modelo</label><select class="form-control"><option>Selecione o modelo</option></select></div>
        <div class="form-group"><label>Ano</label><select class="form-control"><option>Ano do veículo</option></select></div>
      </div>
      <div class="form-row cols-3">
        <div class="form-group"><label>CEP</label><input class="form-control" placeholder="77000-000"></div>
        <div class="form-group"><label>Uso principal</label><select class="form-control"><option>Particular</option><option>Aplicativo</option><option>Comercial</option></select></div>
        <div class="form-group"><label>CPF do condutor</label><input class="form-control" placeholder="000.000.000-00"></div>
      </div>
      <div class="form-actions" style="justify-content:flex-start">
        <button class="btn btn-primary">{umbrella}Calcular cotação</button>
      </div>
    </div>'''.format(umbrella=ICONS["umbrella"])

    plans = ""
    for nome, preco, periodo, itens, destaque in PLANOS:
        cls = "card-pad" + (' style="border:2px solid var(--green-500);position:relative"' if destaque else "")
        tag = '<span class="badge badge-green" style="position:absolute;top:-12px;left:24px">Mais popular</span>' if destaque else ""
        itens_html = "".join(['<li style="display:flex;gap:8px;margin-bottom:10px;font-size:13.5px;color:var(--gray-600)"><span style="color:var(--green-600)">{}</span>{}</li>'.format(ICONS["check-circle"], i) for i in itens])
        btn_cls = "btn-primary" if destaque else "btn-outline-dark"
        plans += '''
        <div class="card card-pad" style="{border}position:relative">
          {tag}
          <h4 style="font-size:15px;color:var(--gray-500);text-transform:uppercase;letter-spacing:.04em">{nome}</h4>
          <div style="margin:10px 0 18px"><span style="font-family:var(--font-display);font-size:32px;font-weight:700;color:var(--navy-900)">{preco}</span><span class="small">{periodo}</span></div>
          <ul style="margin-bottom:20px">{itens}</ul>
          <a href="#" class="btn {btn_cls} btn-block">Contratar plano</a>
        </div>'''.format(border="border:2px solid var(--green-500);" if destaque else "", tag=tag, nome=nome,
                          preco=preco, periodo=periodo, itens=itens_html, btn_cls=btn_cls)

    plans_grid = '<div class="grid-3">{plans}</div>'.format(plans=plans)
    content = '<div class="container" style="padding:36px 0 80px">{form}{plans}</div>'.format(form=form, plans=plans_grid)
    body = navbar("servicos") + header + content + footer()
    return html_shell("Cotar seguro", body, "Compare e contrate seguro auto em Palmas-TO com a AutoPalmas.")


def build_sobre():
    header = page_header([("Início", "index.html"), ("Sobre nós", None)], "Sobre a AutoPalmas",
                          "Conectando compradores, vendedores e empresas em Palmas-TO desde 2024")

    intro = '''
    <div class="grid-2" style="align-items:center;margin-bottom:60px">
      <div>
        <span class="eyebrow">Nossa missão</span>
        <h2 style="font-size:28px">Tornar a compra e venda de veículos mais simples e segura</h2>
        <p>A AutoPalmas nasceu para resolver um problema comum em Palmas-TO: encontrar um carro bom, com um vendedor confiável, sem perder tempo com anúncios duvidosos. Hoje conectamos milhares de compradores a lojas e vendedores verificados, além de oferecer seguro, financiamento e outros serviços em um só lugar.</p>
        <div class="flex gap-12" style="margin-top:20px">
          <div><strong style="font-family:var(--font-display);font-size:26px;color:var(--navy-900)">+25 mil</strong><p class="small">Compradores ativos</p></div>
          <div style="margin-left:30px"><strong style="font-family:var(--font-display);font-size:26px;color:var(--navy-900)">+500</strong><p class="small">Lojas verificadas</p></div>
          <div style="margin-left:30px"><strong style="font-family:var(--font-display);font-size:26px;color:var(--navy-900)">2024</strong><p class="small">Ano de fundação</p></div>
        </div>
      </div>
      <div class="card card-pad">
        <h4 style="margin-bottom:14px">O que nos move</h4>
        <p style="margin-bottom:10px">{s} <strong>Confiança</strong> — verificação real de lojas e anúncios.</p>
        <p style="margin-bottom:10px">{c} <strong>Simplicidade</strong> — encontrar e vender um carro em poucos passos.</p>
        <p style="margin-bottom:0">{h} <strong>Proximidade</strong> — atendimento humano, local, em Palmas-TO.</p>
      </div>
    </div>'''.format(s=ICONS["shield-check"], c=ICONS["check-circle"], h=ICONS["headset"])

    team = ""
    for nome, cargo, seed in [("Marina Alves", "Fundadora & CEO", 0), ("Diego Ferreira", "Head de Produto", 1), ("Ana Beatriz Lima", "Head de Operações", 2), ("Lucas Martins", "Head de Tecnologia", 3)]:
        team += '''
        <div class="text-center">
          <div style="width:84px;height:84px;margin:0 auto 14px">{av}</div>
          <h4 style="font-size:15px;margin-bottom:2px">{nome}</h4>
          <p class="small">{cargo}</p>
        </div>'''.format(av=avatar(nome, size=84, seed=seed), nome=nome, cargo=cargo)

    team_section = '''
    <div class="section-title"><h2>Time <span class="accent">AutoPalmas</span></h2></div>
    <div class="grid-3" style="grid-template-columns:repeat(4,1fr);margin-bottom:60px">{team}</div>
    '''.replace("{team}", team)

    cta = '''
    <div class="cta-banner">
      <div style="position:absolute;inset:0;opacity:.5">{sky}</div>
      <div style="position:relative;grid-column:1/-1;text-align:center">
        <h3 style="text-align:center">Quer fazer parte da <span class="accent">AutoPalmas?</span></h3>
        <p style="margin:0 auto 20px;max-width:480px;text-align:center">Estamos sempre em busca de pessoas e empresas parceiras para crescer em Palmas-TO e região.</p>
        <div class="flex gap-12" style="justify-content:center">
          <a href="cadastro.html" class="btn btn-primary">Criar minha conta</a>
          <a href="empresa-cadastro.html" class="btn btn-outline-light">Cadastrar minha empresa</a>
        </div>
      </div>
    </div>'''.format(sky=cta_skyline())

    content = '<div class="container" style="padding:40px 0 30px">{intro}{team}</div><div class="container" style="margin-bottom:80px">{cta}</div>'.format(intro=intro, team=team_section, cta=cta)
    body = navbar("sobre") + header + content + footer()
    return html_shell("Sobre nós", body, "Conheça a missão, os números e o time da AutoPalmas.")


if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for fname, fn in [("servicos.html", build_servicos), ("seguros.html", build_seguros), ("sobre.html", build_sobre)]:
        out = fn()
        with open(os.path.join(base, fname), "w", encoding="utf-8") as f:
            f.write(out)
        print("wrote", fname, len(out))
