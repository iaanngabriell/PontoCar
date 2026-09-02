# PontoCar — Correção e ordenação de fotos

Este pacote deve ser aplicado **depois** do pacote `PontoCar_Ajustes_Veiculos_Moeda.zip`.

## O que foi corrigido

- Corrige o bloco de upload que estava com texto cortado/overflow.
- Reduz e padroniza as miniaturas em uma grade responsiva.
- Em anúncio novo, as fotos selecionadas podem ser reordenadas por arrastar e soltar ou pelas setas.
- A ordem escolhida para fotos novas é preservada no `input[type=file]`, portanto o serviço atual grava as imagens nessa ordem.
- A primeira foto de anúncio novo é a capa.
- Em edição, fotos já cadastradas aparecem no formulário e podem ser reordenadas.
- A ordem das fotos cadastradas é salva automaticamente por endpoint POST protegido por login + CSRF.
- Somente o proprietário do veículo pode alterar a ordem.
- Ao reordenar fotos já cadastradas, a primeira foto passa a ser `principal=True` e as demais ficam `principal=False`.
- O limite de 8 fotos considera também as fotos já existentes.
- Nenhum model foi alterado e nenhuma migration é necessária.

## Arquivos

- `apps/veiculos/urls.py`
- `apps/veiculos/foto_views.py`
- `apps/veiculos/foto_services.py`
- `templates/veiculos/vendedor_form.html`
- `static/css/ajustes_veiculos.css`
- `static/js/ajustes_fotos.js`

## Validação

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
```

Esperado:

```text
System check identified no issues (0 silenced).
No changes detected
```

## Teste — anúncio novo

1. Abra `/vendedor/veiculos/novo/`.
2. Selecione 3 ou 4 fotos.
3. Confirme que as miniaturas não ficam gigantes e que o texto do upload não é cortado.
4. Arraste a foto 3 para a posição 1, ou use as setas.
5. A primeira miniatura deve mostrar `Capa`.
6. Salve/publica o anúncio.
7. Abra os detalhes e confirme a mesma ordem.

## Teste — anúncio existente

1. Abra `/vendedor/veiculos/<uuid>/editar/`.
2. As fotos já gravadas devem aparecer em `Fotos cadastradas`.
3. Arraste uma foto ou use as setas.
4. Deve aparecer `Salvando ordem…` e depois `Ordem salva.`.
5. A foto na primeira posição vira capa.
6. Recarregue a página e confirme que a ordem permanece.

### Observação sobre novas fotos em edição

Novas imagens são adicionadas após as fotos já cadastradas. Depois de salvar o anúncio, elas passam a integrar a galeria cadastrada e podem ser colocadas em qualquer posição ao reabrir a edição.
