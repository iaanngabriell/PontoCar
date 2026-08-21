# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from partials import navbar, footer, html_shell, dash_page
from icons import ICONS
from illustrations import car_card_illustration

def build_comprador_interesses():
    cards = ""
    data = [("Toyota Corolla XEi 2.0", "R$ 128.900", "Auto Show Veículos", ("Aguardando resposta","badge-amber"), 4),
            ("Hyundai Creta Platinum", "R$ 132.500", "Palmas Motors", ("Respondido","badge-green"), 3),
            ("Jeep Compass Longitude", "R$ 152.400", "Auto Show Veículos", ("Aguardando resposta","badge-amber"), 5)]
    for nome, preco, loja, status, seed in data:
        cards += '''
        <div class="card vehicle-card">
          <div class="vehicle-photo">{illus}
            <span class="badge {cls}" style="position:absolute;top:12px;left:12px">{label}</span>
          </div>
          <div class="vehicle-body">
            <div class="price">{preco}</div>
            <h4>{nome}</h4>
            <p class="small" style="margin-bottom:14px">{building}{loja}</p>
            <div class="vehicle-footer">
              <a href="veiculo-detalhes.html" class="btn btn-outline-dark btn-sm">Ver anúncio</a>
              <a href="#" class="btn btn-primary btn-sm">{whats}Conversar</a>
            </div>
          </div>
        </div>'''.format(illus=car_card_illustration(seed), cls=status[1], label=status[0], preco=preco, nome=nome,
                          building=ICONS["building"], loja=loja, whats=ICONS["phone"])

    content = '''
    <div class="tabs">
      <a href="#" class="active">Interesses enviados (3)</a>
      <a href="#">Favoritos (7)</a>
    </div>
    <div class="vehicle-grid">{cards}</div>'''.format(cards=cards)
    body = dash_page("comprador", "comprador-interesses.html", "Meus interesses", "Acompanhe os veículos que você demonstrou interesse", content)
    return html_shell("Meus interesses", body, "Veículos e leads enviados na AutoPalmas.")

def build_comprador_cotacoes():
    rows = ""
    for seguradora, veiculo, plano, valor, status in [
        ("Seguros Capital", "Toyota Corolla XEi 2.0", "Completo", "R$ 149/mês", ("Ativa","badge-green")),
        ("TO Corretora de Seguros", "Honda HR-V EXL", "Essencial", "R$ 89/mês", ("Em análise","badge-amber")),
        ("Seguros Capital", "Fiat Toro Freedom", "Premium", "R$ 219/mês", ("Expirada","badge-gray")),
    ]:
        rows += '''
        <tr>
          <td class="cell-title">{seg}</td>
          <td>{veiculo}</td>
          <td>{plano}</td>
          <td>{valor}</td>
          <td><span class="badge {cls}">{label}</span></td>
          <td><div class="row-actions"><a href="seguros.html" title="Ver">{eye}</a></div></td>
        </tr>'''.format(seg=seguradora, veiculo=veiculo, plano=plano, valor=valor, cls=status[1], label=status[0], eye=ICONS["eye"])

    content = '''
    <div class="panel">
      <div class="panel-body">
        <table class="data-table">
          <thead><tr><th>Seguradora</th><th>Veículo</th><th>Plano</th><th>Valor</th><th>Status</th><th></th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>'''.format(rows=rows)
    actions = '<a href="seguros.html" class="btn btn-primary btn-sm">{plus}Nova cotação</a>'.format(plus=ICONS["plus"])
    body = dash_page("comprador", "comprador-cotacoes.html", "Minhas cotações", "Cotações de seguro solicitadas por você", content, actions)
    return html_shell("Minhas cotações", body, "Cotações de seguro auto na AutoPalmas.")

def build_comprador_compras():
    rows = ""
    for veiculo, loja, data_, valor, seed in [
        ("Chevrolet Onix LTZ", "Palmas Motors", "22/01/2026", "R$ 78.900", 0),
        ("Renault Kwid Zen", "Auto Show Veículos", "03/11/2025", "R$ 58.900", 1),
    ]:
        rows += '''
        <tr>
          <td><div class="cell-main"><div style="width:42px;height:42px;border-radius:8px;overflow:hidden">{illus}</div><div class="cell-title">{veiculo}</div></div></td>
          <td>{loja}</td>
          <td>{data}</td>
          <td>{valor}</td>
          <td><span class="badge badge-green">{c}Concluída</span></td>
        </tr>'''.format(illus=car_card_illustration(seed), veiculo=veiculo, loja=loja, data=data_, valor=valor, c=ICONS["check-circle"])

    content = '''
    <div class="panel">
      <div class="panel-body">
        <table class="data-table">
          <thead><tr><th>Veículo</th><th>Vendedor</th><th>Data</th><th>Valor</th><th>Status</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>'''.format(rows=rows)
    body = dash_page("comprador", "comprador-compras.html", "Minhas compras", "Histórico de veículos comprados pela plataforma", content)
    return html_shell("Minhas compras", body, "Histórico de compras na AutoPalmas.")

if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for fname, fn in [("comprador-interesses.html", build_comprador_interesses),
                       ("comprador-cotacoes.html", build_comprador_cotacoes),
                       ("comprador-compras.html", build_comprador_compras)]:
        out = fn()
        with open(os.path.join(base, fname), "w", encoding="utf-8") as f:
            f.write(out)
        print("wrote", fname, len(out))
