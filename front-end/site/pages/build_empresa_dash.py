# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from partials import navbar, footer, html_shell, dash_page
from icons import ICONS
from illustrations import car_card_illustration, company_mark

def stat_card(icon, value, label, delta=None):
    d = '<span class="delta">{}</span>'.format(delta) if delta else ""
    return '''
    <div class="stat-card">
      <div class="top"><div class="icon">{icon}</div>{delta}</div>
      <div class="value">{value}</div>
      <div class="label">{label}</div>
    </div>'''.format(icon=ICONS[icon], value=value, label=label, delta=d)

def build_empresa_cadastro():
    content = '''
    <div class="tabs">
      <a href="#" class="active">Dados da empresa</a>
      <a href="empresa-verificacao.html">Verificação / Selo</a>
    </div>
    <div class="panel">
      <div class="panel-header"><h3>Informações gerais</h3></div>
      <div class="panel-body">
        <div class="form-row cols-2">
          <div class="form-group"><label>Razão social</label><input class="form-control" value="Auto Show Comércio de Veículos LTDA"></div>
          <div class="form-group"><label>Nome fantasia</label><input class="form-control" value="Auto Show Veículos"></div>
        </div>
        <div class="form-row cols-2">
          <div class="form-group"><label>CNPJ</label><input class="form-control" value="12.345.678/0001-90"></div>
          <div class="form-group"><label>Categoria</label><select class="form-control"><option>Concessionária</option><option>Revendedora</option><option>Oficina mecânica</option><option>Seguradora</option><option>Corretora de seguros</option><option>Lava-jato</option></select></div>
        </div>
        <div class="form-row cols-2">
          <div class="form-group"><label>Telefone</label><input class="form-control" value="(63) 3212-4477"></div>
          <div class="form-group"><label>WhatsApp comercial</label><input class="form-control" value="(63) 99123-0000"></div>
        </div>
        <div class="form-group" style="margin-bottom:0"><label>Descrição da empresa</label><textarea class="form-control" rows="3">Concessionária multimarcas em Palmas-TO, ativa desde 2016.</textarea></div>
      </div>
    </div>

    <div class="panel">
      <div class="panel-header"><h3>Endereço</h3></div>
      <div class="panel-body">
        <div class="form-row cols-3">
          <div class="form-group"><label>CEP</label><input class="form-control" value="77015-002"></div>
          <div class="form-group" style="grid-column:span 2"><label>Endereço</label><input class="form-control" value="Av. Teotônio Segurado, 1450"></div>
        </div>
        <div class="form-row cols-3">
          <div class="form-group"><label>Bairro</label><input class="form-control" value="Plano Diretor Sul"></div>
          <div class="form-group"><label>Cidade</label><input class="form-control" value="Palmas"></div>
          <div class="form-group"><label>Estado</label><input class="form-control" value="TO"></div>
        </div>
      </div>
    </div>
    <div class="form-actions"><button class="btn btn-outline-dark">Cancelar</button><button class="btn btn-primary">Salvar dados da empresa</button></div>
    '''
    body = dash_page("empresa", "empresa-cadastro.html", "Dados da empresa", "Mantenha as informações da sua empresa atualizadas", content)
    return html_shell("Dados da empresa", body, "Cadastro de empresa parceira AutoPalmas.")

def build_empresa_verificacao():
    content = '''
    <div class="tabs">
      <a href="empresa-cadastro.html">Dados da empresa</a>
      <a href="#" class="active">Verificação / Selo</a>
    </div>
    <div class="panel">
      <div class="panel-header">
        <h3>Status da verificação</h3>
        <span class="badge badge-green">{shield}Selo de confiança ativo</span>
      </div>
      <div class="panel-body">
        <p style="margin-bottom:18px">Sua empresa foi verificada em <strong>12/03/2026</strong>. O selo de confiança aumenta a credibilidade dos seus anúncios e aparece em todos eles.</p>
        <div class="progress-track">
          <div class="seg done"></div><div class="seg done"></div><div class="seg done"></div><div class="seg done"></div>
        </div>
        <div class="grid-2">
          <div class="flex items-center gap-8"><span style="color:var(--green-600)">{check}</span> CNPJ validado na Receita Federal</div>
          <div class="flex items-center gap-8"><span style="color:var(--green-600)">{check}</span> Documento de identidade do responsável</div>
          <div class="flex items-center gap-8"><span style="color:var(--green-600)">{check}</span> Comprovante de endereço comercial</div>
          <div class="flex items-center gap-8"><span style="color:var(--green-600)">{check}</span> Análise manual da equipe AutoPalmas</div>
        </div>
      </div>
    </div>

    <div class="panel">
      <div class="panel-header"><h3>Documentos enviados</h3></div>
      <div class="panel-body">
        <table class="data-table">
          <thead><tr><th>Documento</th><th>Enviado em</th><th>Status</th></tr></thead>
          <tbody>
            <tr><td>Cartão CNPJ</td><td>10/03/2026</td><td><span class="badge badge-green">{c}Aprovado</span></td></tr>
            <tr><td>RG do responsável legal</td><td>10/03/2026</td><td><span class="badge badge-green">{c}Aprovado</span></td></tr>
            <tr><td>Comprovante de endereço</td><td>11/03/2026</td><td><span class="badge badge-green">{c}Aprovado</span></td></tr>
          </tbody>
        </table>
        <label class="upload-box" style="display:block;margin-top:18px;cursor:pointer">
          <div class="icon">{upload}</div>
          <strong>Enviar novo documento</strong>
          <p class="small" style="margin:4px 0 0">PDF, JPG ou PNG, até 8MB</p>
        </label>
      </div>
    </div>'''.format(shield=ICONS["shield-check"], check=ICONS["check-circle"], c=ICONS["check-circle"], upload=ICONS["upload"])
    body = dash_page("empresa", "empresa-verificacao.html", "Verificação / Selo", "Documentos e status do selo de confiança", content)
    return html_shell("Verificação da empresa", body, "Status de verificação e selo de confiança AutoPalmas.")

def build_empresa_dashboard():
    stats = stat_card("car", "24", "Veículos ativos", "+3 este mês") + \
            stat_card("wrench", "5", "Serviços cadastrados") + \
            stat_card("users", "63", "Leads recebidos", "+14 esta semana") + \
            stat_card("money", "R$ 412 mil", "Em vendas fechadas")

    rows = ""
    for nome, preco, status, seed in [("Toyota Corolla XEi 2.0", "R$ 128.900", ("Disponível","badge-green"), 4),
                                        ("Honda HR-V EXL", "R$ 104.500", ("Disponível","badge-green"), 2),
                                        ("Fiat Toro Freedom", "R$ 118.900", ("Reservado","badge-amber"), 5)]:
        rows += '''
        <tr>
          <td><div class="cell-main"><div style="width:42px;height:42px;border-radius:8px;overflow:hidden">{illus}</div><div class="cell-title">{nome}</div></div></td>
          <td>{preco}</td>
          <td><span class="badge {cls}">{label}</span></td>
        </tr>'''.format(illus=car_card_illustration(seed), nome=nome, preco=preco, cls=status[1], label=status[0])

    table = '''
    <div class="panel">
      <div class="panel-header"><h3>Veículos em destaque</h3><a href="vendedor-veiculos.html" class="small" style="font-weight:600">Ver todos</a></div>
      <div class="panel-body"><table class="data-table"><thead><tr><th>Veículo</th><th>Preço</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></div>
    </div>'''.format(rows=rows)

    seal = '''
    <div class="panel">
      <div class="panel-header"><h3>Selo de confiança</h3></div>
      <div class="panel-body flex items-center gap-12">
        <div class="company-logo" style="width:52px;height:52px;flex-shrink:0">{mark}</div>
        <div style="flex:1">
          <span class="badge badge-green">{shield}Verificada</span>
          <p class="small" style="margin:6px 0 0">Sua empresa está com o selo de confiança ativo, aumentando a confiança dos compradores.</p>
        </div>
        <a href="empresa-verificacao.html" class="btn btn-outline-dark btn-sm">Ver detalhes</a>
      </div>
    </div>'''.format(mark=company_mark("AS", 52), shield=ICONS["shield-check"])

    content = '<div class="stat-cards">{stats}</div>{table}{seal}'.format(stats=stats, table=table, seal=seal)
    actions = '<a href="vendedor-veiculo-form.html" class="btn btn-primary btn-sm">{plus}Novo veículo</a>'.format(plus=ICONS["plus"])
    body = dash_page("empresa", "empresa-dashboard.html", "Painel da Auto Show Veículos", "Visão geral da sua empresa na AutoPalmas", content, actions)
    return html_shell("Painel da empresa", body, "Painel da empresa parceira AutoPalmas.")

if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for fname, fn in [("empresa-cadastro.html", build_empresa_cadastro),
                       ("empresa-verificacao.html", build_empresa_verificacao),
                       ("empresa-dashboard.html", build_empresa_dashboard)]:
        out = fn()
        with open(os.path.join(base, fname), "w", encoding="utf-8") as f:
            f.write(out)
        print("wrote", fname, len(out))
