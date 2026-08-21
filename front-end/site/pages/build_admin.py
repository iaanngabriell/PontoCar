# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from partials import navbar, footer, html_shell, dash_page
from icons import ICONS
from illustrations import car_card_illustration, company_mark, avatar

def stat_card(icon, value, label, delta=None, down=False):
    d = '<span class="delta{}">{}</span>'.format(" down" if down else "", delta) if delta else ""
    return '''
    <div class="stat-card">
      <div class="top"><div class="icon">{icon}</div>{delta}</div>
      <div class="value">{value}</div>
      <div class="label">{label}</div>
    </div>'''.format(icon=ICONS[icon], value=value, label=label, delta=d)

def build_admin_dashboard():
    stats = stat_card("users", "25.412", "Usuários cadastrados", "+312 esta semana") + \
            stat_card("building", "527", "Empresas ativas", "+8 este mês") + \
            stat_card("doc-check", "43", "Anúncios em análise", "-12%", True) + \
            stat_card("money", "R$ 2,4 mi", "Vendas no mês", "+9%")

    queue = ""
    for nome, empresa, seed in [("Toyota Corolla XEi 2.0", "Auto Show Veículos", 4), ("Honda Civic Touring", "Palmas Motors", 1), ("Fiat Toro Freedom", "Vendedor particular", 5)]:
        queue += '''
        <tr>
          <td><div class="cell-main"><div style="width:42px;height:42px;border-radius:8px;overflow:hidden">{illus}</div><div class="cell-title">{nome}</div></div></td>
          <td>{empresa}</td>
          <td><span class="badge badge-amber">{clock}Pendente</span></td>
          <td><div class="row-actions"><a href="admin-moderacao.html" title="Revisar">{eye}</a></div></td>
        </tr>'''.format(illus=car_card_illustration(seed), nome=nome, empresa=empresa, clock=ICONS["clock"], eye=ICONS["eye"])

    panel1 = '''
    <div class="panel">
      <div class="panel-header"><h3>Fila de moderação</h3><a href="admin-moderacao.html" class="small" style="font-weight:600">Ver todos</a></div>
      <div class="panel-body"><table class="data-table"><thead><tr><th>Anúncio</th><th>Origem</th><th>Status</th><th></th></tr></thead><tbody>{q}</tbody></table></div>
    </div>'''.format(q=queue)

    verifs = ""
    for nome, seed_color in [("Speed Lava-Jato", "#2ea043"), ("TO Corretora de Seguros", "#1a3a5c")]:
        verifs += '''
        <tr>
          <td><div class="cell-main"><div style="width:36px;height:36px">{mark}</div><div class="cell-title">{nome}</div></div></td>
          <td><span class="badge badge-blue">{doc}Documentos enviados</span></td>
          <td><div class="row-actions"><a href="admin-empresas.html" title="Revisar">{eye}</a></div></td>
        </tr>'''.format(mark=company_mark("".join([w[0] for w in nome.split()[:2]]).upper(), 36, seed_color), nome=nome, doc=ICONS["doc-check"], eye=ICONS["eye"])

    panel2 = '''
    <div class="panel">
      <div class="panel-header"><h3>Empresas aguardando verificação</h3><a href="admin-empresas.html" class="small" style="font-weight:600">Ver todas</a></div>
      <div class="panel-body"><table class="data-table"><thead><tr><th>Empresa</th><th>Status</th><th></th></tr></thead><tbody>{v}</tbody></table></div>
    </div>'''.format(v=verifs)

    content = '<div class="stat-cards">{stats}</div>{p1}{p2}'.format(stats=stats, p1=panel1, p2=panel2)
    body = dash_page("admin", "admin-dashboard.html", "Painel administrativo", "Visão geral da plataforma AutoPalmas", content)
    return html_shell("Painel administrativo", body, "Painel de administração AutoPalmas.")

def build_admin_moderacao():
    rows = ""
    for nome, autor, tipo, seed in [
        ("Toyota Corolla XEi 2.0", "Auto Show Veículos", "Empresa", 4),
        ("Honda Civic Touring", "Palmas Motors", "Empresa", 1),
        ("Fiat Toro Freedom", "Vendedor particular · Marcos Lima", "Particular", 5),
        ("Volkswagen Polo TSI", "Vendedor particular · Sandra Reis", "Particular", 2),
    ]:
        rows += '''
        <tr>
          <td><div class="cell-main"><div style="width:42px;height:42px;border-radius:8px;overflow:hidden">{illus}</div><div><div class="cell-title">{nome}</div><div class="cell-sub">{tipo}</div></div></div></td>
          <td>{autor}</td>
          <td><span class="badge badge-amber">{clock}Pendente</span></td>
          <td><div class="row-actions">
            <a href="#" title="Aprovar" style="color:var(--green-600)">{check}</a>
            <a href="#" title="Rejeitar" style="color:var(--red-500)">{x}</a>
            <a href="veiculo-detalhes.html" title="Ver anúncio">{eye}</a>
          </div></td>
        </tr>'''.format(illus=car_card_illustration(seed), nome=nome, tipo=tipo, autor=autor, clock=ICONS["clock"],
                         check=ICONS["check-circle"], x=ICONS["x-circle"], eye=ICONS["eye"])

    content = '''
    <div class="tabs">
      <a href="#" class="active">Pendentes (43)</a>
      <a href="#">Aprovados hoje (18)</a>
      <a href="#">Rejeitados (3)</a>
    </div>
    <div class="panel">
      <div class="panel-body">
        <table class="data-table">
          <thead><tr><th>Anúncio</th><th>Anunciante</th><th>Status</th><th></th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>'''.format(rows=rows)
    body = dash_page("admin", "admin-moderacao.html", "Moderação de anúncios", "Revise e aprove os anúncios enviados pelos usuários", content)
    return html_shell("Moderação de anúncios", body, "Fila de moderação de anúncios AutoPalmas.")

def build_admin_empresas():
    rows = ""
    for nome, cnpj, status, seed_color in [
        ("Auto Show Veículos", "12.345.678/0001-90", ("Verificada","badge-green"), "#3ebd52"),
        ("Palmas Motors", "23.456.789/0001-11", ("Verificada","badge-green"), "#3577d4"),
        ("Speed Lava-Jato", "34.567.890/0001-22", ("Documentos enviados","badge-blue"), "#2ea043"),
        ("TO Corretora de Seguros", "45.678.901/0001-33", ("Documentos enviados","badge-blue"), "#1a3a5c"),
        ("Oficina do Zé", "56.789.012/0001-44", ("Pendente","badge-amber"), "#e2a02f"),
    ]:
        initials = "".join([w[0] for w in nome.split()[:2]]).upper()
        rows += '''
        <tr>
          <td><div class="cell-main"><div style="width:36px;height:36px">{mark}</div><div class="cell-title">{nome}</div></div></td>
          <td>{cnpj}</td>
          <td><span class="badge {cls}">{label}</span></td>
          <td><div class="row-actions">
            <a href="#" title="Aprovar selo" style="color:var(--green-600)">{check}</a>
            <a href="empresa-detalhes.html" title="Ver empresa">{eye}</a>
          </div></td>
        </tr>'''.format(mark=company_mark(initials, 36, seed_color), nome=nome, cnpj=cnpj, cls=status[1], label=status[0],
                         check=ICONS["check-circle"], eye=ICONS["eye"])

    content = '''
    <div class="tabs">
      <a href="#" class="active">Todas (527)</a>
      <a href="#">Verificadas (498)</a>
      <a href="#">Aguardando análise (21)</a>
      <a href="#">Pendentes (8)</a>
    </div>
    <div class="panel">
      <div class="panel-body">
        <table class="data-table">
          <thead><tr><th>Empresa</th><th>CNPJ</th><th>Status</th><th></th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>'''.format(rows=rows)
    body = dash_page("admin", "admin-empresas.html", "Verificação de empresas", "Aprove documentos e conceda o selo de confiança", content)
    return html_shell("Verificação de empresas", body, "Verificação de empresas parceiras AutoPalmas.")

def build_admin_usuarios():
    rows = ""
    for nome, email, tipo, status, seed in [
        ("Camila Rocha", "camila.rocha@email.com", "Vendedor particular", ("Ativo","badge-green"), 0),
        ("Rafael Nunes", "rafael.nunes@email.com", "Comprador", ("Ativo","badge-green"), 1),
        ("Auto Show Veículos", "contato@autoshow.com.br", "Empresa", ("Ativo","badge-green"), 2),
        ("Diego Ferreira", "diego.ferreira@email.com", "Comprador", ("Suspenso","badge-red"), 3),
        ("Sandra Reis", "sandra.reis@email.com", "Vendedor particular", ("Ativo","badge-green"), 4),
    ]:
        rows += '''
        <tr>
          <td><div class="cell-main">{av}<div><div class="cell-title">{nome}</div><div class="cell-sub">{email}</div></div></div></td>
          <td>{tipo}</td>
          <td><span class="badge {cls}">{label}</span></td>
          <td><div class="row-actions"><a href="#" title="Ver">{eye}</a><a href="#" title="Suspender">{x}</a></div></td>
        </tr>'''.format(av='<div style="width:36px;height:36px">'+avatar(nome,36,seed)+'</div>', nome=nome, email=email,
                         tipo=tipo, cls=status[1], label=status[0], eye=ICONS["eye"], x=ICONS["x-circle"])

    content = '''
    <div class="panel">
      <div class="panel-header">
        <h3>Todos os usuários</h3>
        <input class="form-control" placeholder="Buscar por nome ou e-mail" style="width:260px">
      </div>
      <div class="panel-body">
        <table class="data-table">
          <thead><tr><th>Usuário</th><th>Perfil</th><th>Status</th><th></th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>'''.format(rows=rows)
    body = dash_page("admin", "admin-usuarios.html", "Usuários", "Gerencie compradores, vendedores e empresas cadastradas", content)
    return html_shell("Usuários", body, "Gestão de usuários AutoPalmas.")

def build_admin_vendas():
    rows = ""
    for veiculo, comprador, vendedor, valor, data_, seed in [
        ("Chevrolet Onix LTZ", "Rafael Nunes", "Palmas Motors", "R$ 78.900", "22/01/2026", 0),
        ("Renault Kwid Zen", "Fernanda Dias", "Auto Show Veículos", "R$ 58.900", "03/11/2025", 1),
        ("Honda HR-V EXL", "Eduardo Castro", "Auto Show Veículos", "R$ 104.500", "18/10/2025", 2),
    ]:
        rows += '''
        <tr>
          <td><div class="cell-main"><div style="width:42px;height:42px;border-radius:8px;overflow:hidden">{illus}</div><div class="cell-title">{veiculo}</div></div></td>
          <td>{comprador}</td>
          <td>{vendedor}</td>
          <td>{valor}</td>
          <td>{data}</td>
        </tr>'''.format(illus=car_card_illustration(seed), veiculo=veiculo, comprador=comprador, vendedor=vendedor, valor=valor, data=data_)

    stats = stat_card("money", "R$ 2,4 mi", "Vendas no mês", "+9%") + \
            stat_card("handshake", "312", "Negócios fechados") + \
            stat_card("car", "R$ 96,4 mil", "Ticket médio")

    content = '''
    <div class="stat-cards" style="grid-template-columns:repeat(3,1fr)">{stats}</div>
    <div class="panel">
      <div class="panel-body">
        <table class="data-table">
          <thead><tr><th>Veículo</th><th>Comprador</th><th>Vendedor</th><th>Valor</th><th>Data</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>'''.format(stats=stats, rows=rows)
    body = dash_page("admin", "admin-vendas.html", "Vendas", "Histórico de negócios fechados na plataforma", content)
    return html_shell("Vendas", body, "Histórico de vendas na AutoPalmas.")

if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for fname, fn in [("admin-dashboard.html", build_admin_dashboard),
                       ("admin-moderacao.html", build_admin_moderacao),
                       ("admin-empresas.html", build_admin_empresas),
                       ("admin-usuarios.html", build_admin_usuarios),
                       ("admin-vendas.html", build_admin_vendas)]:
        out = fn()
        with open(os.path.join(base, fname), "w", encoding="utf-8") as f:
            f.write(out)
        print("wrote", fname, len(out))
