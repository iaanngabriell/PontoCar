# PontoCar — Ajustes Bloco 1

Este pacote foi preparado a partir do código enviado em `bloco1_codigo.txt`.

## O que foi corrigido

1. **Botão Painel**
   - Empresa -> `/empresa/dashboard/`
   - Vendedor -> `/vendedor/veiculos/`
   - Comprador -> `/comprador/compras/`
   - Administração -> `/gestao/usuarios/`

2. **Criar conta some quando o usuário está logado**
   - Usuário autenticado vê Painel, Perfil e Sair.
   - Visitante vê Entrar e Criar conta.
   - Logout continua sendo POST + CSRF.

3. **Login e cadastro**
   - Templates foram alinhados às classes que já existem no design system (`auth-wrap`, `auth-visual`, `auth-form-side`).
   - Erros são exibidos próximos aos campos.
   - Campos ganharam autocomplete, placeholders e máscaras visuais.

4. **Cadastro de empresa**
   - Criado/substituído o arquivo correto: `templates/empresas/empresa_cadastro.html`.
   - A view usa exatamente esse nome.
   - O formulário agora apresenta dados comerciais e localização reais do Django.
   - CNPJ e CEP são normalizados/validados.

5. **Senha ao criar empresa**
   - Não foi criada senha no model `Empresa`.
   - Ao escolher **Sou empresa** no cadastro, o usuário cria e confirma sua senha normalmente e é redirecionado para `/empresa/cadastro/`.
   - A empresa usa a conta do representante para autenticação.

6. **Navbar ao clicar em Vender**
   - `base_dashboard.html` agora mantém a navbar pública acima do dashboard.
   - Assim, telas do fluxo do vendedor que estendem `base_dashboard.html` preservam a barra de navegação.

## Como aplicar

Extraia o ZIP na raiz do projeto PontoCar e aceite substituir os arquivos existentes.

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

## Testes rápidos

### Visitante
- `/` -> deve mostrar Entrar + Criar conta.
- `/entrar/` -> formulário deve estar alinhado e responsivo.
- `/cadastro/` -> selecionar Comprar/Vender/Empresa deve destacar a opção.

### Usuário logado
- `/` -> Criar conta não deve aparecer.
- Perfil deve abrir pelo ícone de usuário.
- Painel deve levar ao fluxo correspondente ao tipo do usuário.

### Cadastro empresa
1. Sair da conta.
2. Abrir `/cadastro/`.
3. Selecionar **Sou empresa**.
4. Preencher nome, e-mail e senha.
5. Após criar conta, deve redirecionar automaticamente para `/empresa/cadastro/`.
6. Preencher CNPJ, categoria, contato e localização.
7. Salvar -> deve abrir `/empresa/dashboard/`.
8. A mesma senha criada no passo 4 continua sendo a credencial da conta representante.

### Vender
- Clique em Vender na navbar.
- A rota `/vendedor/veiculos/novo/` deve abrir.
- Se a tela usa `base_dashboard.html`, a navbar pública continua visível acima do painel.
