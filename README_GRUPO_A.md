# PontoCar — Conversão Django — Grupo A

Este pacote contém a primeira conversão do front-end estático para Django Templates.

## Páginas convertidas

- index
- sobre
- login
- cadastro
- perfil
- alterar-senha
- empresas
- empresa-cadastro
- empresa-dashboard
- servicos
- comprador-compras
- vendedor-leads
- admin-usuarios
- admin-vendas

## O que foi adicionado

- `templates/base.html` e `templates/base_dashboard.html`
- componentes compartilhados em `templates/components/`
- `forms.py`, `views.py` e `urls.py` para os apps envolvidos
- assets em `static/css/style.css` e `static/js/app.js`
- roteamento central em `config/urls.py`
- configurações de login/logout em `config/settings.py`
- `apps/empresas/services.py` para salvar empresa + localização em transação atômica

## Decisões preservadas

- nenhuma alteração em models;
- nenhuma migration necessária;
- nenhuma transição de status é feita diretamente pelas views;
- operações administrativas desta etapa são somente leitura;
- campos que existiam apenas no mockup, mas não no model (`WhatsApp comercial` separado e `descrição da empresa`), não foram persistidos/inventados;
- logout usa POST + CSRF;
- a marca visual foi normalizada de AutoPalmas para PontoCar.

## Rotas ainda pendentes

Alguns links do menu apontam para páginas do Grupo B, que ainda não foram convertidas (`/catalogo/`, `/vendedor/veiculos/novo/`, `/comprador/interesses/`, `/seguros/` etc.). Esses links só ficarão ativos após o próximo grupo.

## Aplicação

Copie o conteúdo deste pacote para a raiz do repositório, preservando os caminhos. Os arquivos `config/settings.py`, `config/urls.py` e os `views.py` listados são substituições completas.

Depois, no PowerShell com o `.venv` ativo:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py runserver
```

O segundo comando deve informar que não há mudanças de model.

## Validação já feita neste ambiente

- sintaxe de todos os arquivos Python: OK (`py_compile`);
- contagem básica de delimitadores dos templates: OK;
- nenhuma migration criada;
- nenhuma referência residual a `AutoPalmas` ou `Lava-jato` no pacote.

Não foi possível executar `python manage.py check` aqui porque o runtime de ferramentas não possui Django instalado nem acesso ao `.venv` local do projeto.

## Observação sobre empresa

O model permite várias empresas por representante, mas o mockup do Grupo A apresenta um único painel/dados de empresa sem seletor. Esta etapa usa a primeira empresa do usuário como empresa corrente. Se o MVP realmente permitir administrar várias empresas simultaneamente pelo mesmo representante, o próximo refinamento deve adicionar seleção de empresa/UUID na URL antes de consolidar esse fluxo.
