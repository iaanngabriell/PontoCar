# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from partials import navbar, footer, html_shell, page_header
from icons import ICONS
from illustrations import car_card_illustration

VEHICLES = [
    ("Toyota Corolla XEi 2.0", "2023/2023", "34.000 km", "Automático", "Flex", "R$ 128.900", 4, "Disponível"),
    ("Hyundai Creta Platinum", "2022/2023", "28.500 km", "Automático", "Flex", "R$ 132.500", 3, "Disponível"),
    ("Chevrolet Onix LTZ", "2021/2022", "41.200 km", "Manual", "Flex", "R$ 78.900", 0, "Disponível"),
    ("Jeep Compass Longitude", "2022/2022", "38.700 km", "Automático", "Diesel", "R$ 152.400", 5, "Reservado"),
    ("Volkswagen Polo TSI", "2023/2024", "12.300 km", "Automático", "Flex", "R$ 98.700", 1, "Disponível"),
    ("Fiat Toro Freedom", "2021/2021", "52.900 km", "Automático", "Diesel", "R$ 118.900", 2, "Disponível"),
    ("Honda HR-V EXL", "2020/2021", "61.400 km", "Automático", "Flex", "R$ 104.500", 4, "Disponível"),
    ("Renault Kwid Zen", "2022/2023", "19.800 km", "Manual", "Flex", "R$ 58.900", 0, "Disponível"),
    ("Nissan Kicks SV", "2021/2022", "45.100 km", "Automático", "Flex", "R$ 96.300", 3, "Disponível"),
]

def vehicle_card(nome, ano, km, cambio, comb, preco, seed, status):
    badge_cls = "badge-green" if status == "Disponível" else "badge-amber"
    return '''
        <div class="card vehicle-card">
          <div class="vehicle-photo">{illus}<a href="#" class="fav">{heart}</a>
            <span class="badge {badge_cls}" style="position:absolute;top:12px;left:12px">{status}</span>
          </div>
          <div class="vehicle-body">
            <div class="price">{preco}</div>
            <h4>{nome}</h4>
            <div class="vehicle-meta">
              <span>{cal}{ano}</span><span>{gauge}{km}</span><span>{gear}{cambio}</span><span>{fuel}{comb}</span>
            </div>
            <div class="vehicle-footer">
              <span class="seller">{pin}Palmas-TO</span>
              <a href="veiculo-detalhes.html" class="btn btn-outline-dark btn-sm">Ver detalhes</a>
            </div>
          </div>
        </div>'''.format(illus=car_card_illustration(seed), heart=ICONS["heart"], preco=preco, nome=nome,
                          cal=ICONS["calendar"], ano=ano, gauge=ICONS["gauge"], km=km, gear=ICONS["gearbox"],
                          cambio=cambio, fuel=ICONS["fuel"], comb=comb, pin=ICONS["pin"], badge_cls=badge_cls, status=status)

def build():
    header = page_header([("Início", "index.html"), ("Comprar", None)], "Catálogo de veículos",
                          "9.482 anúncios disponíveis em Palmas-TO e região")

    filters = '''
    <aside class="filter-box">
      <div class="flex items-center justify-between" style="margin-bottom:6px">
        <h4>{filter} Filtros</h4>
        <a href="catalogo.html" class="small">Limpar</a>
      </div>
      <div class="filter-group">
        <div class="filter-title">Marca</div>
        <select class="form-control"><option>Todas as marcas</option><option>Toyota</option><option>Hyundai</option><option>Chevrolet</option><option>Jeep</option><option>Volkswagen</option></select>
      </div>
      <div class="filter-group">
        <div class="filter-title">Modelo</div>
        <select class="form-control"><option>Todos os modelos</option></select>
      </div>
      <div class="filter-group">
        <div class="filter-title">Ano</div>
        <div class="form-row cols-2" style="margin-bottom:0">
          <select class="form-control"><option>De</option></select>
          <select class="form-control"><option>Até</option></select>
        </div>
      </div>
      <div class="filter-group">
        <div class="filter-title" id="preco-max-label">Preço · até R$ 200.000</div>
        <input type="range" id="preco-max" min="20000" max="400000" step="1000" value="200000" style="width:100%">
      </div>
      <div class="filter-group">
        <div class="filter-title">Câmbio</div>
        <div class="check-list">
          <label><input type="checkbox" checked> Automático</label>
          <label><input type="checkbox"> Manual</label>
        </div>
      </div>
      <div class="filter-group">
        <div class="filter-title">Combustível</div>
        <div class="check-list">
          <label><input type="checkbox"> Flex</label>
          <label><input type="checkbox"> Diesel</label>
          <label><input type="checkbox"> Híbrido/Elétrico</label>
        </div>
      </div>
      <div class="filter-group">
        <div class="filter-title">Vendedor</div>
        <div class="check-list">
          <label><input type="checkbox"> Lojas com selo de confiança</label>
          <label><input type="checkbox"> Anúncios de particulares</label>
        </div>
      </div>
      <button class="btn btn-primary btn-block">Aplicar filtros</button>
    </aside>'''.format(filter=ICONS["sliders"])

    cards = "".join([vehicle_card(*v) for v in VEHICLES])

    results = '''
    <div>
      <div class="results-bar">
        <p><strong>9.482</strong> veículos encontrados</p>
        <select class="form-control" style="width:auto">
          <option>Mais relevantes</option>
          <option>Menor preço</option>
          <option>Maior preço</option>
          <option>Mais recentes</option>
          <option>Menor quilometragem</option>
        </select>
      </div>
      <div class="vehicle-grid">{cards}</div>
      <div class="pagination">
        <a href="#">{prev}</a>
        <a href="#" class="active">1</a><a href="#">2</a><a href="#">3</a><span>…</span><a href="#">42</a>
        <a href="#">{next}</a>
      </div>
    </div>'''.format(cards=cards, prev="&larr;", next="&rarr;")

    layout = '<div class="container" style="padding:36px 0 80px"><div class="catalog-layout">{filters}{results}</div></div>'.format(filters=filters, results=results)

    body = navbar("comprar") + header + layout + footer()
    return html_shell("Catálogo de veículos", body, "Busque veículos por marca, modelo, ano, preço e mais em Palmas-TO.")

if __name__ == "__main__":
    out = build()
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "catalogo.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    print("wrote", path, len(out))
