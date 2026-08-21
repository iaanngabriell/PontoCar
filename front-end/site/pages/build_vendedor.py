# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from partials import navbar, footer, html_shell, dash_page
from icons import ICONS
from illustrations import car_card_illustration, avatar

def stat_card(icon, value, label, delta=None, down=False):
    d = ""
    if delta:
        d = '<span class="delta{}">{}</span>'.format(" down" if down else "", delta)
    return '''
    <div class="stat-card">
      <div class="top"><div class="icon">{icon}</div>{delta}</div>
      <div class="value">{value}</div>
      <div class="label">{label}</div>
    </div>'''.format(icon=ICONS[icon], value=value, label=label, delta=d)

def build_vendedor_dashboard():
    stats = stat_card("car", "12", "Anúncios ativos", "+2 este mês") + \
            stat_card("users", "38", "Leads recebidos", "+9 esta semana") + \
            stat_card("eye", "4.2 mil", "Visualizações", "+18%") + \
            stat_card("handshake", "5", "Vendas concluídas")

    rows = ""
    for nome, preco, status, seed in [("Toyota Corolla XEi 2.0", "R$ 128.900", ("Disponível","badge-green"), 4),
                                        ("Jeep Compass Longitude", "R$ 152.400", ("Reservado","badge-amber"), 5),
                                        ("Chevrolet Onix LTZ", "R$ 78.900", ("Vendido","badge-gray"), 0)]:
        rows += '''
        <tr>
          <td><div class="cell-main"><div style="width:42px;height:42px;border-radius:8px;overflow:hidden">{illus}</div><div><div class="cell-title">{nome}</div><div class="cell-sub">{preco}</div></div></div></td>
          <td><span class="badge {cls}">{label}</span></td>
          <td>6 leads</td>
          <td><div class="row-actions"><a href="vendedor-veiculo-form.html">{edit}</a><a href="veiculo-detalhes.html">{eye}</a></div></td>
        </tr>'''.format(illus=car_card_illustration(seed), nome=nome, preco=preco, cls=status[1], label=status[0],
                         edit=ICONS["edit"], eye=ICONS["eye"])

    table = '''
    <div class="panel">
      <div class="panel-header"><h3>Meus anúncios recentes</h3><a href="vendedor-veiculos.html" class="small" style="font-weight:600">Ver todos</a></div>
      <div class="panel-body">
        <table class="data-table">
          <thead><tr><th>Veículo</th><th>Status</th><th>Interesse</th><th></th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>'''.format(rows=rows)

    leads_panel = '''
    <div class="panel">
      <div class="panel-header"><h3>Últimos leads</h3><a href="vendedor-leads.html" class="small" style="font-weight:600">Ver todos</a></div>
      <div class="panel-body">
        <table class="data-table">
          <thead><tr><th>Interessado</th><th>Veículo</th><th>Recebido</th></tr></thead>
          <tbody>
          <tr><td><div class="cell-main">{av1}<div class="cell-title">Rafael Nunes</div></div></td><td>Toyota Corolla XEi</td><td>há 2h</td></tr>
          <tr><td><div class="cell-main">{av2}<div class="cell-title">Priscila Gomes</div></div></td><td>Jeep Compass</td><td>há 5h</td></tr>
          <tr><td><div class="cell-main">{av3}<div class="cell-title">Eduardo Castro</div></div></td><td>Toyota Corolla XEi</td><td>ontem</td></tr>
          </tbody>
        </table>
      </div>
    </div>'''.format(av1='<div style="width:34px;height:34px">'+avatar("Rafael Nunes",34,0)+'</div>',
                      av2='<div style="width:34px;height:34px">'+avatar("Priscila Gomes",34,1)+'</div>',
                      av3='<div style="width:34px;height:34px">'+avatar("Eduardo Castro",34,2)+'</div>')

    content = '<div class="stat-cards">{stats}</div>{table}{leads}'.format(stats=stats, table=table, leads=leads_panel)
    actions = '<a href="vendedor-veiculo-form.html" class="btn btn-primary btn-sm">{plus}Novo anúncio</a>'.format(plus=ICONS["plus"])
    body = dash_page("vendedor", "vendedor-dashboard.html", "Olá, Camila", "Acompanhe seus anúncios e leads em um só lugar", content, actions)
    return html_shell("Painel do vendedor", body, "Painel do vendedor AutoPalmas.")

def build_vendedor_veiculos():
    rows = ""
    data = [("Toyota Corolla XEi 2.0", "R$ 128.900", ("Disponível","badge-green"), "34.000 km · 2023", 4),
            ("Jeep Compass Longitude", "R$ 152.400", ("Reservado","badge-amber"), "38.700 km · 2022", 5),
            ("Chevrolet Onix LTZ", "R$ 78.900", ("Vendido","badge-gray"), "41.200 km · 2021", 0),
            ("Hyundai Creta Platinum", "R$ 132.500", ("Em análise","badge-blue"), "28.500 km · 2022", 3),
            ("Volkswagen Polo TSI", "R$ 98.700", ("Disponível","badge-green"), "12.300 km · 2023", 1)]
    for nome, preco, status, meta, seed in data:
        rows += '''
        <tr>
          <td><div class="cell-main"><div style="width:42px;height:42px;border-radius:8px;overflow:hidden">{illus}</div><div><div class="cell-title">{nome}</div><div class="cell-sub">{meta}</div></div></div></td>
          <td>{preco}</td>
          <td><span class="badge {cls}">{label}</span></td>
          <td><div class="row-actions"><a href="vendedor-veiculo-form.html" title="Editar">{edit}</a><a href="veiculo-detalhes.html" title="Ver anúncio">{eye}</a><a href="#" title="Excluir">{trash}</a></div></td>
        </tr>'''.format(illus=car_card_illustration(seed), nome=nome, meta=meta, preco=preco, cls=status[1],
                         label=status[0], edit=ICONS["edit"], eye=ICONS["eye"], trash=ICONS["trash"])

    content = '''
    <div class="tabs">
      <a href="#" class="active">Todos (12)</a>
      <a href="#">Disponíveis (8)</a>
      <a href="#">Reservados (2)</a>
      <a href="#">Vendidos (1)</a>
      <a href="#">Em análise (1)</a>
    </div>
    <div class="panel">
      <div class="panel-body">
        <table class="data-table">
          <thead><tr><th>Veículo</th><th>Preço</th><th>Status</th><th></th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>'''.format(rows=rows)
    actions = '<a href="vendedor-veiculo-form.html" class="btn btn-primary btn-sm">{plus}Novo anúncio</a>'.format(plus=ICONS["plus"])
    body = dash_page("vendedor", "vendedor-veiculos.html", "Meus veículos", "Gerencie todos os seus anúncios", content, actions)
    return html_shell("Meus veículos", body, "Gerencie seus veículos anunciados na AutoPalmas.")

def build_vendedor_veiculo_form():
    content = '''
    <div class="grid-2" style="grid-template-columns:1.6fr 1fr;align-items:flex-start">
      <div>
        <div class="panel">
          <div class="panel-header"><h3>Dados do veículo</h3></div>
          <div class="panel-body">
            <div class="form-row cols-3">
              <div class="form-group"><label>Marca</label><select class="form-control"><option>Toyota</option></select></div>
              <div class="form-group"><label>Modelo</label><input class="form-control" value="Corolla XEi 2.0"></div>
              <div class="form-group"><label>Versão</label><input class="form-control" value="XEi 2.0 Flex"></div>
            </div>
            <div class="form-row cols-3">
              <div class="form-group"><label>Ano fabricação</label><input class="form-control" value="2022"></div>
              <div class="form-group"><label>Ano modelo</label><input class="form-control" value="2023"></div>
              <div class="form-group"><label>Quilometragem</label><input class="form-control" value="34000"></div>
            </div>
            <div class="form-row cols-3">
              <div class="form-group"><label>Câmbio</label><select class="form-control"><option>Automático</option><option>Manual</option></select></div>
              <div class="form-group"><label>Combustível</label><select class="form-control"><option>Flex</option><option>Diesel</option><option>Híbrido/Elétrico</option></select></div>
              <div class="form-group"><label>Cor</label><input class="form-control" value="Prata Ice"></div>
            </div>
            <div class="form-row cols-2">
              <div class="form-group"><label>Preço (R$)</label><input class="form-control" value="128900"></div>
              <div class="form-group"><label>Placa (final)</label><input class="form-control" value="3"></div>
            </div>
            <div class="form-group" style="margin-bottom:0"><label>Descrição e opcionais</label><textarea class="form-control" rows="4">Único dono, todas as revisões em concessionária, pneus novos.</textarea></div>
          </div>
        </div>

        <div class="panel">
          <div class="panel-header"><h3>Fotos do veículo</h3></div>
          <div class="panel-body">
            <label for="foto-upload" class="upload-box" style="display:block;cursor:pointer">
              <div class="icon">{upload}</div>
              <strong>Clique para enviar fotos</strong>
              <p class="small" style="margin:4px 0 0">PNG ou JPG, até 10 fotos, 8MB cada</p>
              <input id="foto-upload" type="file" multiple accept="image/*" style="display:none">
            </label>
            <div class="photo-grid" id="photo-grid">
              <div class="photo-thumb">{c0}<span class="main-tag">Capa</span><span class="remove">{x}</span></div>
              <div class="photo-thumb">{c1}<span class="remove">{x}</span></div>
              <div class="photo-thumb">{c2}<span class="remove">{x}</span></div>
            </div>
          </div>
        </div>
      </div>

      <div>
        <div class="panel">
          <div class="panel-header"><h3>Status do anúncio</h3></div>
          <div class="panel-body">
            <div class="form-group"><label>Situação</label>
              <select class="form-control"><option>Disponível</option><option>Reservado</option><option>Vendido</option><option>Pausado</option></select>
            </div>
            <p class="small">Anúncios passam por uma checagem rápida da nossa equipe antes de ficarem públicos.</p>
          </div>
        </div>
        <div class="form-actions" style="justify-content:flex-start;flex-direction:column;align-items:stretch;gap:10px">
          <button class="btn btn-primary btn-block">Publicar anúncio</button>
          <button class="btn btn-outline-dark btn-block">Salvar como rascunho</button>
        </div>
      </div>
    </div>'''.format(upload=ICONS["upload"], x=ICONS["x-circle"],
                      c0=car_card_illustration(4), c1=car_card_illustration(0), c2=car_card_illustration(2))
    body = dash_page("vendedor", "vendedor-veiculo-form.html", "Novo anúncio", "Preencha os dados do veículo que deseja anunciar", content)
    return html_shell("Novo anúncio", body, "Anuncie seu veículo na AutoPalmas.")

def build_vendedor_leads():
    rows = ""
    data = [("Rafael Nunes", "Toyota Corolla XEi", "(63) 99123-4567", "há 2h", 0),
            ("Priscila Gomes", "Jeep Compass Longitude", "(63) 98877-1122", "há 5h", 1),
            ("Eduardo Castro", "Toyota Corolla XEi", "(63) 99911-2233", "ontem", 2),
            ("Fernanda Dias", "Hyundai Creta Platinum", "(63) 99222-8899", "há 2 dias", 3)]
    for nome, veiculo, tel, quando, seed in data:
        rows += '''
        <tr>
          <td><div class="cell-main">{av}<div><div class="cell-title">{nome}</div><div class="cell-sub">{tel}</div></div></div></td>
          <td>{veiculo}</td>
          <td>{quando}</td>
          <td><div class="row-actions"><a href="#" title="WhatsApp">{whats}</a><a href="#" title="E-mail">{mail}</a></div></td>
        </tr>'''.format(av='<div style="width:34px;height:34px">'+avatar(nome,34,seed)+'</div>', nome=nome, tel=tel,
                         veiculo=veiculo, quando=quando, whats=ICONS["phone"], mail=ICONS["mail"])

    content = '''
    <div class="panel">
      <div class="panel-body">
        <table class="data-table">
          <thead><tr><th>Interessado</th><th>Veículo</th><th>Recebido</th><th></th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>'''.format(rows=rows)
    body = dash_page("vendedor", "vendedor-leads.html", "Leads recebidos", "Pessoas interessadas nos seus anúncios", content)
    return html_shell("Leads recebidos", body, "Veja quem demonstrou interesse nos seus veículos.")

if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for fname, fn in [("vendedor-dashboard.html", build_vendedor_dashboard),
                       ("vendedor-veiculos.html", build_vendedor_veiculos),
                       ("vendedor-veiculo-form.html", build_vendedor_veiculo_form),
                       ("vendedor-leads.html", build_vendedor_leads)]:
        out = fn()
        with open(os.path.join(base, fname), "w", encoding="utf-8") as f:
            f.write(out)
        print("wrote", fname, len(out))
