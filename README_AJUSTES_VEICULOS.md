# PontoCar — Ajustes de moeda, placa e formulário de veículo

Este pacote deve ser aplicado sobre a branch `feature/ajustes-interface-servicos`, depois do Bloco 1 e da gestão de serviços.

## O que foi ajustado

### 1. Formatação monetária pt-BR
- Novo filtro de template `brl`: `128900` -> `R$ 128.900,00`.
- Novo filtro `numero_br` para quilometragem e outros números inteiros: `34000` -> `34.000`.
- Valores de veículos, serviços, seguros, apólices e vendas foram padronizados nas telas incluídas no pacote.
- Campos de preço de veículo e serviço aceitam entradas como:
  - `128900`
  - `128900,50`
  - `128.900,50`
  - `R$ 128.900,50`
- Ao sair do campo, a interface reapresenta o valor no formato brasileiro.

### 2. Placa em maiúsculas
- O back-end já normalizava a placa com `.upper()`; essa regra foi preservada.
- O campo agora também transforma visualmente a placa em maiúsculas durante a digitação.
- Caracteres de separação são removidos pelo back-end antes de salvar.
- A validação de placa duplicada foi preservada.

### 3. Formulário Vender reorganizado
O formulário foi dividido em seções:
1. Identificação
2. Ano e uso
3. Características
4. Preço e placa
5. Descrição e opcionais
6. Fotos
7. Finalização

A descrição ganhou uma área maior e contador de caracteres. O limite de fotos continua em 8 arquivos, com até 8 MB por foto.

### 4. Campos do veículo
Todos os campos editáveis existentes no model continuam disponíveis no formulário:
- marca
- modelo
- versão
- ano de fabricação
- ano do modelo
- quilometragem
- câmbio
- combustível
- cor
- preço
- placa
- descrição

`quantidade_proprietarios` não foi transformado em campo manual. Esse dado é gerenciado pelo histórico/vendas do sistema e passa a ser exibido na página de detalhes do veículo.

## Arquivos novos
- `apps/core/formatters.py`
- `apps/core/form_fields.py`
- `static/css/ajustes_veiculos.css`

## Arquivos substituídos
- `apps/core/templatetags/pontocar_tags.py`
- `apps/veiculos/forms.py`
- `apps/servicos/forms.py`
- `static/js/ajustes_bloco1.js`
- templates de veículos e telas que exibem moeda incluídas neste pacote.

## Banco de dados
Nenhum model foi alterado e nenhuma migration deve ser criada.

## Validação

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py runserver
```

Esperado:

```text
System check identified no issues (0 silenced).
No changes detected
```

## Teste principal
1. Acesse `/vendedor/veiculos/novo/`.
2. Digite `128900` no preço e saia do campo: deve aparecer `128.900,00`.
3. Digite `abc1d23` na placa: deve aparecer `ABC1D23`.
4. Preencha o anúncio e salve.
5. Confirme no catálogo/detalhes que o valor aparece como `R$ 128.900,00`.
6. Edite o anúncio e confirme que o campo de preço reaparece formatado.
7. Em uma conta Empresa, crie/edite um serviço usando `180,00` ou `1.250,50` e confirme a exibição pt-BR no catálogo público.
