# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from partials import navbar, footer, html_shell
from icons import ICONS
from illustrations import hero_illustration, cta_skyline, car_card_illustration

def build():
    hero = '''
  <section class="hero">
    <div class="container">
      <div class="hero-grid">
        <div>
          <span class="eyebrow">Palmas · Tocantins</span>
          <h1>Seu próximo carro<span class="accent">está aqui.</span></h1>
          <p class="lead">As melhores ofertas de lojas confiáveis em Palmas-TO e região. Compre com segurança, venda com facilidade e conte com serviços que fazem a diferença.</p>
          <div class="hero-cta">
            <a href="catalogo.html" class="btn btn-primary">{search}Buscar veículos</a>
            <a href="vendedor-veiculo-form.html" class="btn btn-outline-light">{tag}Quero vender meu carro</a>
          </div>
        </div>
        <div class="hero-photo">{illustration}</div>
      </div>

      <div class="trust-strip">
        <div class="trust-item">{shield}<div><strong>Lojas verificadas</strong><span>Mais segurança para você</span></div></div>
        <div class="trust-item">{award}<div><strong>Selo de Confiança</strong><span>Perfis verificados</span></div></div>
        <div class="trust-item">{headset}<div><strong>Atendimento rápido</strong><span>Fale com quem resolve</span></div></div>
        <div class="trust-item">{lock}<div><strong>100% Seguro</strong><span>Seus dados protegidos</span></div></div>
      </div>
    </div>
  </section>

  <div class="container">
    <div class="search-card">
      <h3>Encontre o carro <span class="accent">ideal</span> para você</h3>
      <div class="search-grid">
        <div class="field"><label>Marca</label><select class="form-control"><option>Todas as marcas</option><option>Toyota</option><option>Volkswagen</option><option>Chevrolet</option><option>Hyundai</option><option>Fiat</option></select></div>
        <div class="field"><label>Modelo</label><select class="form-control"><option>Todos os modelos</option></select></div>
        <div class="field"><label>Ano de</label><select class="form-control"><option>Ano mínimo</option></select></div>
        <div class="field"><label>Ano até</label><select class="form-control"><option>Ano máximo</option></select></div>
        <div class="field"><label>Preço</label><select class="form-control"><option>Faixa de preço</option></select></div>
      </div>
      <div class="search-actions">
        <a href="catalogo.html" class="link-advanced">{sliders}Busca avançada</a>
        <a href="catalogo.html" class="btn btn-primary">Buscar agora{search}</a>
      </div>
    </div>
  </div>
'''.format(search=ICONS["search"], tag=ICONS["handshake"], illustration=hero_illustration(),
           shield=ICONS["shield-check"], award=ICONS["award"], headset=ICONS["headset"], lock=ICONS["lock"],
           sliders=ICONS["sliders"])

    why = '''
  <section class="section">
    <div class="container">
      <div class="section-title">
        <h2>Por que escolher a <span class="accent">AutoPalmas</span>?</h2>
      </div>
      <div class="feature-grid">
        <div><div class="feature-icon">{shield}</div><h4>Confiança</h4><p>Lojas e anúncios verificados para você comprar com tranquilidade.</p></div>
        <div><div class="feature-icon">{car}</div><h4>Melhores oportunidades</h4><p>Encontre carros com preços justos e condições que cabem no seu bolso.</p></div>
        <div><div class="feature-icon">{headset}</div><h4>Atendimento humano</h4><p>Fale direto com o lojista e tire todas as suas dúvidas de forma rápida e fácil.</p></div>
        <div><div class="feature-icon">{doc}</div><h4>Serviços integrados</h4><p>Cote seguros e encontre serviços parceiros sem sair da plataforma.</p></div>
      </div>
    </div>
  </section>
'''.format(shield=ICONS["shield-check"], car=ICONS["car"], headset=ICONS["headset"], doc=ICONS["doc-check"])

    how = '''
  <section class="section section-tight" id="como-funciona" style="background:#fff">
    <div class="container">
      <div class="section-title">
        <h2><span class="accent">Como</span> funciona</h2>
      </div>
      <div class="steps">
        <div class="step"><div class="step-icon">{search}<span class="step-num">01</span></div><h4>Encontre</h4><p>Busque entre milhares de veículos com filtros avançados.</p></div>
        <div class="step"><div class="step-icon">{chat}<span class="step-num">02</span></div><h4>Fale com o lojista</h4><p>Entre em contato direto e tire suas dúvidas com facilidade.</p></div>
        <div class="step"><div class="step-icon">{shield}<span class="step-num">03</span></div><h4>Compre com segurança</h4><p>Lojas verificadas e nosso selo de confiança protegem você.</p></div>
        <div class="step"><div class="step-icon">{car}<span class="step-num">04</span></div><h4>Aproveite seu novo carro</h4><p>Finalize o negócio e curta seu novo carro com tranquilidade.</p></div>
      </div>
    </div>
  </section>
'''.format(search=ICONS["search"], chat=ICONS["headset"], shield=ICONS["shield-check"], car=ICONS["car"])

    destaques_cards = ""
    sample = [
        ("Toyota Corolla XEi 2.0", "2023/2023", "34.000 km", "Automático", "R$ 128.900", 4),
        ("Hyundai Creta Platinum", "2022/2023", "28.500 km", "Automático", "R$ 132.500", 3),
        ("Chevrolet Onix LTZ", "2021/2022", "41.200 km", "Manual", "R$ 78.900", 0),
    ]
    for nome, ano, km, cambio, preco, seed in sample:
        destaques_cards += '''
        <div class="card vehicle-card">
          <div class="vehicle-photo">{illus}<a href="#" class="fav">{heart}</a></div>
          <div class="vehicle-body">
            <div class="price">{preco}</div>
            <h4>{nome}</h4>
            <div class="vehicle-meta">
              <span>{cal}{ano}</span><span>{gauge}{km}</span><span>{gear}{cambio}</span>
            </div>
            <div class="vehicle-footer">
              <span class="seller">{pin} Palmas - TO</span>
              <a href="veiculo-detalhes.html" class="btn btn-outline-dark btn-sm">Ver detalhes</a>
            </div>
          </div>
        </div>'''.format(illus=car_card_illustration(seed), heart=ICONS["heart"], preco=preco, nome=nome,
                          cal=ICONS["calendar"], ano=ano, gauge=ICONS["gauge"], km=km, gear=ICONS["gearbox"],
                          cambio=cambio, pin=ICONS["pin"])

    destaques = '''
  <section class="section" style="padding-top:16px">
    <div class="container">
      <div class="results-bar">
        <div><h2 style="margin-bottom:2px;font-size:26px">Veículos em destaque</h2><p class="small">Selecionados essa semana em Palmas-TO</p></div>
        <a href="catalogo.html" class="btn btn-outline-dark btn-sm">Ver catálogo completo{arrow}</a>
      </div>
      <div class="vehicle-grid">{cards}</div>
    </div>
  </section>
'''.format(cards=destaques_cards, arrow=ICONS["arrow-right"])

    cta = '''
  <section class="container" style="margin-bottom:80px">
    <div class="cta-banner">
      <div style="position:absolute;inset:0;opacity:.5">{skyline}</div>
      <div style="position:relative">
        <h3>Anuncie seu veículo e<span class="accent">venda mais rápido!</span></h3>
        <p>Milhares de pessoas estão procurando o carro ideal em Palmas-TO e região neste momento.</p>
        <div class="cta-actions">
          <a href="vendedor-veiculo-form.html" class="btn btn-primary">{tag}Anunciar meu carro</a>
          <a href="sobre.html" class="btn btn-outline-light">Saiba mais</a>
        </div>
      </div>
      <div class="cta-stats" style="position:relative">
        <div class="stat"><strong>+25 mil</strong><span>Compradores ativos todos os meses</span></div>
        <div class="stat"><strong>+8 mil</strong><span>Veículos disponíveis na plataforma</span></div>
        <div class="stat"><strong>+500</strong><span>Lojas verificadas com nosso selo de confiança</span></div>
      </div>
    </div>
  </section>
'''.format(skyline=cta_skyline(), tag=ICONS["handshake"])

    body = navbar("") + hero + why + how + destaques + cta + footer()
    return html_shell("Compre e venda veículos em Palmas-TO", body,
                       "Catálogo de veículos, empresas verificadas, serviços automotivos e seguros em Palmas-TO.")

if __name__ == "__main__":
    out = build()
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    print("wrote", path, len(out), "bytes")
