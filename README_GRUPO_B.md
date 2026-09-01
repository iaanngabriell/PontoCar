# PontoCar — Conversão Django — Grupo B

Este pacote é **cumulativo**: contém o Grupo A já validado + o Grupo B. Pode ser sobreposto na raiz do projeto.

## Correção incorporada do Grupo A

As rotas de empresa já estão com os caminhos validados durante os testes:

- `/empresa/cadastro/`
- `/empresa/dashboard/`

## Páginas convertidas no Grupo B

1. `catalogo.html` → `/catalogo/`
2. `veiculo-detalhes.html` → `/veiculos/<uuid>/`
3. `vendedor-veiculo-form.html` → `/vendedor/veiculos/novo/` e edição do próprio anúncio
4. `vendedor-veiculos.html` → `/vendedor/veiculos/`
5. `admin-moderacao.html` → `/gestao/moderacao/`
6. `empresa-verificacao.html` → `/empresa/verificacao/`
7. `comprador-interesses.html` → `/comprador/interesses/`
8. `comprador-cotacoes.html` → `/comprador/cotacoes/`
9. `seguros.html` → `/seguros/`

## Funcionalidades conectadas

### Catálogo e detalhes
- Catálogo público apenas com `DISPONIVEL` e `RESERVADO`.
- Filtros por marca, modelo, ano, preço, câmbio, combustível e tipo de anunciante.
- Ordenação e paginação.
- Fotos reais de `FotoVeiculo`.
- Página de detalhes com galeria, especificações e anunciante.
- Formulário de interesse cria `Lead` real; continua aceitando visitante não autenticado.
- Usuário autenticado pode adicionar/remover `Favorito`.

### Vendedor / empresa
- Cadastro de veículo com até 8 fotos, 8 MB por arquivo.
- Publicação inicial mantém a decisão atual do projeto: novo anúncio publicado entra em `DISPONIVEL`.
- Opção "Salvar como rascunho" cria `RASCUNHO`.
- Rascunho pode ser enviado para análise pelo fluxo existente `RASCUNHO -> EM_ANALISE`.
- Edição de dados do próprio veículo sem alterar o status.
- Listagem por todos os 8 status.
- Pausar, reativar, arquivar, enviar/re-enviar para análise chamam `apps.veiculos.services`.

### Moderação
- Tela mostra os 8 estados de `Veiculo`.
- Usuários com `veiculos.pode_moderar_veiculo` podem acessar e aprovar/rejeitar.
- Aprovação/rejeição usa `apps.veiculos.services`, nunca alteração direta na view.
- Staff/administrador pode consultar; os botões de aprovação/rejeição só aparecem com a permissão específica.

### Verificação de empresa
- Lista os registros reais de `VerificacaoEmpresa`.
- `Empresa.possui_selo_ativo()` determina o selo.
- Upload cria um registro `PENDENTE` por documento.
- Arquivos aceitos: PDF/JPG/PNG, até 8 MB.
- O template não publica link direto para o documento.

### Interesses e favoritos
- Aba "Interesses enviados" usa `Lead` com `comprador=request.user`.
- Aba "Favoritos" usa `Favorito`.
- Um favorito pode ser removido diretamente da página.

### Seguros
- `/seguros/` lista `Seguro` ativo de empresa ativa do tipo `SEGURADORA` ou `CORRETORA`.
- Não foi recriado `CotacaoSeguro`.
- `/comprador/cotacoes/` usa `ApoliceSeguro` e os status reais `ATIVA`, `EXPIRADA`, `CANCELADA`.
- O valor exibido é `valor_mensal` da apólice; no catálogo de planos é `valor_referencia`.
- O formulário de simulação estática do protótipo não grava uma cotação inexistente no domínio atual.

## Arquivos principais adicionados/alterados

- `config/urls.py`
- `apps/veiculos/forms.py`
- `apps/veiculos/services.py`
- `apps/veiculos/urls.py`
- `apps/veiculos/views.py`
- `apps/favoritos/services.py`
- `apps/favoritos/urls.py`
- `apps/favoritos/views.py`
- `apps/seguros/urls.py`
- `apps/seguros/views.py`
- `apps/empresas/forms.py`
- `apps/empresas/services.py`
- `apps/empresas/urls.py`
- `apps/empresas/views.py`
- `apps/core/templatetags/pontocar_tags.py`
- templates do Grupo B e componentes compartilhados
- `static/js/app.js`

## Banco de dados

**Nenhum model foi alterado. Nenhuma migration deve ser criada.**

Depois de copiar o pacote:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
```

Esperado:

```text
System check identified no issues (0 silenced).
No changes detected
```

## Testes funcionais recomendados

### 1. Catálogo

Acesse `/catalogo/`.

- Crie pelo admin veículos `DISPONIVEL`, `RESERVADO`, `VENDIDO`, `PAUSADO`.
- Apenas disponíveis/reservados devem aparecer.
- Teste todos os filtros e a ordenação.
- Clique em detalhes.

### 2. Interesse

Em `/veiculos/<uuid>/`:

- Deslogado: envie nome/e-mail/telefone/mensagem; o `Lead.comprador` deve ficar `NULL`.
- Logado: campos devem vir pré-preenchidos e o `Lead.comprador` deve ser o usuário.
- O lead deve aparecer em `/vendedor/leads/` para o proprietário correto.

### 3. Favoritos

- Logado, favorite um veículo.
- Confira `/comprador/interesses/?aba=favoritos`.
- Remova e confirme que desaparece.

### 4. Novo anúncio + fotos

Entre com usuário `VENDEDOR` ou `EMPRESA` e acesse `/vendedor/veiculos/novo/`.

- Publique com 1–8 fotos: deve criar `Veiculo` + `FotoVeiculo`.
- A primeira foto deve virar principal quando ainda não houver principal.
- Tente 9 fotos: deve exibir erro e não deixar criação parcial.
- Tente arquivo >8 MB: deve falhar.
- Teste placa duplicada: mensagem amigável de veículo já cadastrado.
- Salve outro como rascunho e confirme `RASCUNHO`.

### 5. Meus veículos

Acesse `/vendedor/veiculos/`.

- Confira filtros para os 8 estados.
- Edite o próprio veículo e confirme que o status não muda.
- `DISPONIVEL -> PAUSADO`.
- `PAUSADO -> DISPONIVEL` (reativar).
- `PAUSADO -> ARQUIVADO`.
- `RASCUNHO -> EM_ANALISE`.
- `REJEITADO -> EM_ANALISE`.

### 6. Moderação

- Adicione um usuário ao grupo `Moderador`.
- Acesse `/gestao/moderacao/`.
- Em um veículo `EM_ANALISE`, teste aprovar: deve ir para `DISPONIVEL`.
- Teste outro e rejeite: deve ir para `REJEITADO`.
- Com staff sem `pode_moderar_veiculo`, a tela pode ser consultada, mas os botões não devem aparecer.

### 7. Verificação de empresa

Acesse `/empresa/verificacao/` com representante que possua empresa.

- Envie PDF/JPG/PNG válido.
- Deve criar `VerificacaoEmpresa` como `PENDENTE`.
- Aprove pelo admin e recarregue: deve mostrar `APROVADA` e, se não houver suspensão, selo ativo.
- Rejeite/suspenda registros e confira os badges.

### 8. Interesses do comprador

Acesse `/comprador/interesses/`.

- Leads do próprio comprador aparecem.
- Leads de outro usuário não aparecem.
- Favoritos ficam na aba separada.

### 9. Seguros

- Cadastre `Seguro` ativo em empresa `SEGURADORA` ou `CORRETORA` ativa.
- Confira `/seguros/`.
- Seguro inativo ou empresa inativa não deve aparecer.
- Cadastre `ApoliceSeguro` para um comprador.
- Confira `/comprador/cotacoes/` e filtros `ATIVA`, `EXPIRADA`, `CANCELADA`.

## Validação feita neste ambiente

- Todos os `.py` do pacote passaram por `py_compile`.
- Todas as referências `{% url %}` do pacote possuem rota nomeada correspondente.
- Não restaram links internos para arquivos `.html` nem caminhos antigos das páginas convertidas.
- O runtime deste ambiente não possui Django, portanto `manage.py check` e testes com banco devem ser executados no `.venv` local do projeto.

## Observações de domínio

1. O model atual liga `Veiculo` ao usuário proprietário, não diretamente a uma `Empresa`. Para representantes com várias empresas, a UI continua usando a primeira empresa ativa como contexto, mesma limitação já identificada no Grupo A.
2. `comprador-cotacoes.html` foi reconciliado com `ApoliceSeguro`; não existe status "Em análise" no model atual.
3. O front recebido contém ainda `admin-dashboard.html`, `admin-empresas.html`, `empresa-detalhes.html` e `vendedor-dashboard.html`, mas esses quatro arquivos não aparecem nas listas de Grupo A/Grupo B do resumo consolidado. Eles devem ser tratados em um fechamento separado, sem inventar que faziam parte do Grupo B.
