# PontoCar — Ajustes de Serviços para Empresa

Este pacote deve ser aplicado **depois** do `PontoCar_Ajustes_Bloco1.zip`.

## O que muda

- Footer público permanece no fim da viewport em páginas com pouco conteúdo, mantendo espaço em branco quando necessário.
- Usuário representante de empresa ganha área `Meus serviços`.
- Cadastro, edição e exclusão de serviços.
- Somente serviços da empresa vinculada ao usuário podem ser editados/excluídos.
- Atalho `Novo serviço` no painel da empresa.
- Card `Serviços cadastrados` do painel abre a gestão de serviços.
- A listagem pública mostra `Gerenciar meus serviços` quando o usuário autenticado é do tipo EMPRESA.
- Nenhuma alteração de model ou migration.

## Novas rotas

- `/empresa/servicos/`
- `/empresa/servicos/novo/`
- `/empresa/servicos/<uuid>/editar/`
- `/empresa/servicos/<uuid>/excluir/` (POST)

## Como aplicar

Copie as pastas `apps`, `templates` e `static` para a raiz do projeto e aceite substituir os arquivos existentes.

Depois rode:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py runserver
```

Esperado para migrations: `No changes detected`.

## Teste principal

1. Entre com usuário criado como `Sou empresa`.
2. Abra `Painel`.
3. Clique em `Novo serviço` ou `Meus serviços`.
4. Cadastre nome, descrição, preço e duração.
5. Confirme que aparece em `/empresa/servicos/`.
6. Abra `/servicos/` e confirme que aparece no catálogo público.
7. Edite o serviço.
8. Exclua o serviço e confirme que desaparece do catálogo.

Observação: o projeto atual permite várias empresas por representante, mas ainda não possui seletor de empresa. Assim como o dashboard atual, este fluxo usa a primeira empresa vinculada ao usuário até implementarmos esse seletor.
