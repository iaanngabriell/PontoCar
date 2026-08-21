# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from partials import navbar, footer, html_shell, page_header
from icons import ICONS
from illustrations import car_card_illustration, avatar

def build():
    header = page_header([("Início", "index.html"), ("Comprar", "catalogo.html"), ("Toyota Corolla XEi 2.0", None)],
                          "Toyota Corolla XEi 2.0", "Anúncio verificado · publicado há 4 dias")

    thumbs = "".join(['<img src="data:image/svg+xml;utf8,{}" class="{}">'.format("x", "active" if i==0 else "") for i in range(5)])
    # inline SVGs directly (data URIs are messy) — render as inline <div> wrappers instead
    gallery_thumb_svgs = "".join(
        '<div class="{cls}" style="border-radius:8px;overflow:hidden;border:2px solid {border}">{svg}</div>'.format(
            cls="", border="#3ebd52" if i == 0 else "transparent", svg=car_card_illustration(i)
        ) for i in range(5)
    )

    gallery = '''
    <div class="gallery-main">{main}</div>
    <div class="gallery-thumbs">{thumbs}</div>
    '''.format(main=car_card_illustration(4), thumbs=gallery_thumb_svgs)

    specs = '''
    <div class="spec-grid">
      <div class="spec-item"><span>Marca / Modelo</span><strong>Toyota Corolla</strong></div>
      <div class="spec-item"><span>Versão</span><strong>XEi 2.0 Flex</strong></div>
      <div class="spec-item"><span>Ano fab./modelo</span><strong>2022 / 2023</strong></div>
      <div class="spec-item"><span>Quilometragem</span><strong>34.000 km</strong></div>
      <div class="spec-item"><span>Câmbio</span><strong>Automático CVT</strong></div>
      <div class="spec-item"><span>Combustível</span><strong>Flex</strong></div>
      <div class="spec-item"><span>Cor</span><strong>Prata Ice</strong></div>
      <div class="spec-item"><span>Placa final</span><strong>final 3 (não rodiziada)</strong></div>
      <div class="spec-item"><span>Status</span><strong style="color:var(--green-600)">Disponível</strong></div>
    </div>'''

    description = '''
    <p>Toyota Corolla XEi 2.0 Flex automático, único dono, todas as revisões feitas em concessionária, manual e chave reserva. Veículo revisado, pneus novos e sem detalhes de pintura. Ideal para quem busca economia, conforto e baixa depreciação.</p>
    <div class="check-list" style="display:grid;grid-template-columns:1fr 1fr;gap:10px 20px;margin-top:14px">
      <label>{check} Único dono</label>
      <label>{check} Todas as revisões em concessionária</label>
      <label>{check} Ar-condicionado digital</label>
      <label>{check} Central multimídia</label>
      <label>{check} Piloto automático adaptativo</label>
      <label>{check} Sensor de estacionamento</label>
      <label>{check} Câmera de ré</label>
      <label>{check} Bancos em couro</label>
    </div>'''.format(check='<span style="color:var(--green-600)">{}</span>'.format(ICONS["check-circle"]))

    lead_form = '''
    <form class="card card-pad" style="margin-top:24px">
      <h4 style="margin-bottom:16px">Tenho interesse nesse veículo</h4>
      <div class="form-group" style="margin-bottom:14px"><label>Nome completo</label><input class="form-control" placeholder="Seu nome"></div>
      <div class="form-row cols-2">
        <div class="form-group"><label>E-mail</label><input class="form-control" type="email" placeholder="voce@email.com"></div>
        <div class="form-group"><label>Telefone / WhatsApp</label><input class="form-control" placeholder="(63) 9 0000-0000"></div>
      </div>
      <div class="form-group" style="margin-bottom:16px"><label>Mensagem</label><textarea class="form-control" rows="3">Olá! Tenho interesse neste Toyota Corolla e gostaria de mais informações.</textarea></div>
      <button class="btn btn-primary btn-block" type="submit">{chat} Enviar interesse</button>
      <p class="small text-center" style="margin-top:10px">Seus dados são enviados diretamente ao anunciante.</p>
    </form>'''.format(chat=ICONS["headset"])

    sidebar = '''
    <div class="card card-pad price-box" style="margin-bottom:18px">
      <span class="label">Valor anunciado</span>
      <div class="value">R$ 128.900</div>
      <span class="small">ou financiado a partir de R$ 1.890/mês</span>
    </div>
    <div class="card card-pad seller-card" style="margin-bottom:18px">
      {avatar}
      <h4>Auto Show Veículos</h4>
      <span class="seal">{seal} Selo de confiança</span>
      <p class="small">Concessionária multimarcas em Palmas-TO, ativa desde 2016.</p>
      <a href="empresa-detalhes.html" class="btn btn-outline-dark btn-block btn-sm" style="margin-bottom:8px">Ver loja</a>
      <a href="#" class="btn btn-primary btn-block btn-sm">{whats} Chamar no WhatsApp</a>
    </div>
    <div class="card card-pad">
      <h4 style="font-size:14.5px;margin-bottom:12px">{shield} Compra protegida</h4>
      <p class="small" style="margin-bottom:8px">Lojas verificadas pelo selo de confiança AutoPalmas.</p>
      <p class="small" style="margin-bottom:8px">Histórico do veículo conferido antes da publicação.</p>
      <p class="small margin-bottom:0">Suporte da nossa equipe durante toda a negociação.</p>
    </div>'''.format(avatar='<img class="avatar" src="data:image/svg+xml;utf8,{}" alt="" style="width:66px;height:66px;border-radius:50%;margin:0 auto 12px;display:block">'.format(""),
                      seal=ICONS["shield-check"], whats=ICONS["phone"], shield=ICONS["shield-check"])
    # replace broken data uri avatar with actual inline svg wrapped in div for correct rendering
    sidebar = sidebar.replace(
        '<img class="avatar" src="data:image/svg+xml;utf8,{}" alt="" style="width:66px;height:66px;border-radius:50%;margin:0 auto 12px;display:block">'.format(""),
        '<div style="width:66px;height:66px;margin:0 auto 12px">{}</div>'.format(avatar("Auto Show", size=66))
    )

    content = '''
    <div class="container" style="padding:32px 0 80px">
      <div class="grid-2" style="grid-template-columns: 1.7fr 1fr; align-items:flex-start; gap:32px">
        <div>
          {gallery}
          <div class="card card-pad" style="margin-top:24px">
            <h3 style="font-size:18px">Especificações</h3>
            {specs}
          </div>
          <div class="card card-pad" style="margin-top:24px">
            <h3 style="font-size:18px">Descrição e opcionais</h3>
            {description}
          </div>
          {lead_form}
        </div>
        <div>{sidebar}</div>
      </div>

      <div class="section-title" style="margin-top:70px">
        <h2>Veículos <span class="accent">semelhantes</span></h2>
      </div>
      <div class="vehicle-grid">
        {rel1}{rel2}{rel3}
      </div>
    </div>'''.format(gallery=gallery, specs=specs, description=description, lead_form=lead_form, sidebar=sidebar,
                      rel1=related_card("Toyota Corolla GLi 1.8", "R$ 109.900", 3),
                      rel2=related_card("Toyota Corolla Altis 2.0", "R$ 141.300", 5),
                      rel3=related_card("Honda Civic Touring", "R$ 138.700", 1))

    body = navbar("comprar") + header + content + footer()
    return html_shell("Toyota Corolla XEi 2.0", body, "Toyota Corolla XEi 2.0 automático 2023 à venda em Palmas-TO.")

def related_card(nome, preco, seed):
    return '''
        <div class="card vehicle-card">
          <div class="vehicle-photo">{illus}<a href="#" class="fav">{heart}</a></div>
          <div class="vehicle-body">
            <div class="price">{preco}</div>
            <h4>{nome}</h4>
            <div class="vehicle-footer">
              <span class="seller">{pin}Palmas-TO</span>
              <a href="veiculo-detalhes.html" class="btn btn-outline-dark btn-sm">Ver detalhes</a>
            </div>
          </div>
        </div>'''.format(illus=car_card_illustration(seed), heart=ICONS["heart"], preco=preco, nome=nome, pin=ICONS["pin"])

if __name__ == "__main__":
    out = build()
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "veiculo-detalhes.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    print("wrote", path, len(out))
