# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from partials import navbar, footer, html_shell, page_header, dash_page
from icons import ICONS
from illustrations import avatar

def auth_visual(items, title, subtitle):
    lis = "".join(['<li>{}{}</li>'.format(ICONS["check-circle"], i) for i in items])
    return '''
    <div class="auth-visual">
      <div>
        <a href="index.html" class="brand" style="margin-bottom:40px">
          <svg viewBox="0 0 48 24" width="34" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 16l2.4-7A3 3 0 0 1 7.2 7h17a3 3 0 0 1 2.9 1.8L29 16"/><path d="M2 16h27v5.5a1.5 1.5 0 0 1-1.5 1.5h-1.7a1.5 1.5 0 0 1-1.5-1.5V20H6.7v1.5A1.5 1.5 0 0 1 5.2 23H3.5A1.5 1.5 0 0 1 2 21.5z"/><circle cx="9.5" cy="20.3" r="2"/><circle cx="21" cy="20.3" r="2"/></svg>
          <span><span class="brand-word">Auto<span>Palmas</span></span></span>
        </a>
        <h2 style="color:#fff;font-size:24px">{title}</h2>
        <p style="color:rgba(255,255,255,.65);margin-bottom:26px">{subtitle}</p>
        <ul>{lis}</ul>
      </div>
      <p class="small" style="color:rgba(255,255,255,.4)">© 2026 AutoPalmas · Palmas, Tocantins</p>
    </div>'''.format(title=title, subtitle=subtitle, lis=lis)

def build_login():
    visual = auth_visual(
        ["Anuncie seu veículo em minutos", "Fale direto com compradores e vendedores", "Cote seguro sem sair da plataforma"],
        "Bem-vindo de volta", "Entre para acompanhar seus anúncios, leads e cotações.")
    form = '''
    <div class="auth-form-side">
      <h2>Entrar na sua conta</h2>
      <p style="margin-bottom:24px">Novo por aqui? <a href="cadastro.html" style="color:var(--green-600);font-weight:600">Criar conta grátis</a></p>
      <form>
        <div class="form-group" style="margin-bottom:16px"><label>E-mail</label><input class="form-control" type="email" placeholder="voce@email.com"></div>
        <div class="form-group" style="margin-bottom:10px"><label>Senha</label><input class="form-control" type="password" placeholder="••••••••"></div>
        <div class="flex items-center justify-between" style="margin-bottom:22px">
          <label class="checkbox-row" style="margin:0"><input type="checkbox"> Lembrar de mim</label>
          <a href="#" class="small" style="font-weight:600;color:var(--navy-800)">Esqueci minha senha</a>
        </div>
        <button class="btn btn-primary btn-block" type="submit">Entrar</button>
        <div class="form-divider">ou continue com</div>
        <button class="btn btn-outline-dark btn-block" type="button">Entrar com Google</button>
      </form>
    </div>'''
    body = '<div class="auth-shell"><div class="auth-wrap">{visual}{form}</div></div>'.format(visual=visual, form=form)
    return html_shell("Entrar", navbar("") + body + footer(), "Acesse sua conta AutoPalmas.")

def build_cadastro():
    visual = auth_visual(
        ["Cadastro gratuito e rápido", "Escolha o perfil: comprador, vendedor ou empresa", "Selo de confiança para quem verifica seus dados"],
        "Crie sua conta", "Junte-se a milhares de pessoas comprando e vendendo com segurança.")
    form = '''
    <div class="auth-form-side">
      <h2>Criar conta grátis</h2>
      <p style="margin-bottom:20px">Já tem conta? <a href="login.html" style="color:var(--green-600);font-weight:600">Entrar</a></p>
      <form>
        <div class="form-group" style="margin-bottom:16px">
          <label>Eu quero</label>
          <div class="form-row cols-3" style="margin-bottom:0">
            <label class="card card-pad text-center" style="padding:12px;border-color:var(--green-500);cursor:pointer"><input type="radio" name="tipo" checked style="display:none">{car}<div class="small" style="margin-top:4px;font-weight:700;color:var(--navy-900)">Comprar</div></label>
            <label class="card card-pad text-center" style="padding:12px;cursor:pointer"><input type="radio" name="tipo" style="display:none">{tag}<div class="small" style="margin-top:4px;font-weight:700;color:var(--navy-900)">Vender</div></label>
            <label class="card card-pad text-center" style="padding:12px;cursor:pointer"><input type="radio" name="tipo" style="display:none">{building}<div class="small" style="margin-top:4px;font-weight:700;color:var(--navy-900)">Sou empresa</div></label>
          </div>
        </div>
        <div class="form-row cols-2">
          <div class="form-group"><label>Nome</label><input class="form-control" name="first_name" placeholder="Seu nome"></div>
          <div class="form-group"><label>Sobrenome</label><input class="form-control" name="last_name" placeholder="Seu sobrenome"></div>
        </div>
        <div class="form-row cols-2">
          <div class="form-group"><label>CPF</label><input class="form-control" name="cpf" placeholder="000.000.000-00"></div>
          <div class="form-group"><label>Telefone / WhatsApp</label><input class="form-control" name="telefone" placeholder="(63) 9 0000-0000"></div>
        </div>
        <div class="form-group"><label>E-mail</label><input class="form-control" type="email" name="email" placeholder="voce@email.com"></div>
        <div class="form-row cols-2">
          <div class="form-group"><label>Senha</label><input class="form-control" type="password" placeholder="Mínimo 8 caracteres"></div>
          <div class="form-group"><label>Confirmar senha</label><input class="form-control" type="password" placeholder="Repita a senha"></div>
        </div>
        <label class="checkbox-row" style="margin-bottom:20px"><input type="checkbox"> Li e aceito os <a href="#" style="color:var(--green-600)">termos de uso</a> e a <a href="#" style="color:var(--green-600)">política de privacidade</a></label>
        <button class="btn btn-primary btn-block" type="submit">Criar minha conta</button>
      </form>
    </div>'''.format(car=ICONS["car"], tag=ICONS["handshake"], building=ICONS["building"])
    body = '<div class="auth-shell"><div class="auth-wrap" style="max-width:1020px">{visual}{form}</div></div>'.format(visual=visual, form=form)
    return html_shell("Criar conta", navbar("") + body + footer(), "Crie sua conta gratuita na AutoPalmas.")

def build_perfil():
    content = '''
    <div class="panel">
      <div class="panel-header"><h3>Dados pessoais</h3></div>
      <div class="panel-body">
        <div class="flex items-center gap-12" style="margin-bottom:24px">
          <div style="width:76px;height:76px">{av}</div>
          <div>
            <button class="btn btn-outline-dark btn-sm">{cam}Alterar foto</button>
            <p class="small" style="margin:8px 0 0">JPG ou PNG, até 5MB.</p>
          </div>
        </div>
        <div class="form-row cols-2">
          <div class="form-group"><label>Nome</label><input class="form-control" name="first_name" value="Camila"></div>
          <div class="form-group"><label>Sobrenome</label><input class="form-control" name="last_name" value="Rocha"></div>
        </div>
        <div class="form-row cols-2">
          <div class="form-group"><label>CPF</label><input class="form-control" value="123.456.789-00" disabled></div>
          <div class="form-group"><label>Telefone / WhatsApp</label><input class="form-control" name="telefone" value="(63) 99123-4567"></div>
        </div>
        <div class="form-group" style="margin-bottom:0"><label>E-mail</label><input class="form-control" type="email" name="email" value="camila.rocha@email.com"></div>
        <div class="form-actions"><button class="btn btn-outline-dark">Cancelar</button><button class="btn btn-primary">Salvar alterações</button></div>
      </div>
    </div>
    <div class="panel">
      <div class="panel-header"><h3>Segurança</h3></div>
      <div class="panel-body">
        <div class="flex items-center justify-between">
          <div><strong style="font-size:14.5px">Senha</strong><p class="small" style="margin:2px 0 0">Última alteração há 3 meses</p></div>
          <a href="alterar-senha.html" class="btn btn-outline-dark btn-sm">Alterar senha</a>
        </div>
      </div>
    </div>
    <div class="panel">
      <div class="panel-header"><h3>Notificações</h3></div>
      <div class="panel-body">
        <label class="checkbox-row" style="margin-bottom:12px"><input type="checkbox" checked> Receber e-mails sobre novos leads</label>
        <label class="checkbox-row" style="margin-bottom:12px"><input type="checkbox" checked> Receber WhatsApp sobre mensagens novas</label>
        <label class="checkbox-row"><input type="checkbox"> Receber novidades e promoções da AutoPalmas</label>
      </div>
    </div>'''.format(av=avatar("Camila Rocha", size=76), cam=ICONS["camera"])
    body = dash_page("vendedor", "perfil.html", "Meu perfil", "Gerencie seus dados pessoais e de segurança", content)
    return html_shell("Meu perfil", body, "Gerencie seus dados na AutoPalmas.")

def build_alterar_senha():
    content = '''
    <div class="panel" style="max-width:520px">
      <div class="panel-header"><h3>Alterar senha</h3></div>
      <div class="panel-body">
        <div class="form-group" style="margin-bottom:16px"><label>Senha atual</label><input class="form-control" type="password" placeholder="••••••••"></div>
        <div class="form-group" style="margin-bottom:16px"><label>Nova senha</label><input class="form-control" type="password" placeholder="Mínimo 8 caracteres"></div>
        <div class="form-group" style="margin-bottom:20px"><label>Confirmar nova senha</label><input class="form-control" type="password" placeholder="Repita a nova senha"></div>
        <div class="form-actions"><a href="perfil.html" class="btn btn-outline-dark">Cancelar</a><button class="btn btn-primary">Salvar nova senha</button></div>
      </div>
    </div>'''
    body = dash_page("vendedor", "perfil.html", "Alterar senha", "Mantenha sua conta protegida", content)
    return html_shell("Alterar senha", body, "Altere a senha da sua conta AutoPalmas.")

if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for fname, fn in [("login.html", build_login), ("cadastro.html", build_cadastro),
                       ("perfil.html", build_perfil), ("alterar-senha.html", build_alterar_senha)]:
        out = fn()
        with open(os.path.join(base, fname), "w", encoding="utf-8") as f:
            f.write(out)
        print("wrote", fname, len(out))