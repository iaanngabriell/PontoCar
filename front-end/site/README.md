# AutoPalmas — Protótipo de front-end (HTML/CSS/JS)

Este pacote contém o front-end estático de todas as telas do MVP descritas na
documentação técnica (seção 15.2), no mesmo estilo visual da imagem de
referência enviada (navy + verde, tipografia Poppins/Inter).

## Como abrir
Basta abrir qualquer arquivo `.html` diretamente no navegador — não precisa
de servidor. Comece por `index.html`.

## Estrutura

```
├── index.html                     Home (igual ao print de referência)
├── catalogo.html                  Comprar → listagem de veículos com filtros
├── veiculo-detalhes.html          Detalhes do anúncio + formulário de lead
├── empresas.html                  Diretório de empresas parceiras
├── empresa-detalhes.html          Perfil público de uma empresa
├── servicos.html                  Serviços integrados (financiamento, despachante...)
├── seguros.html                   Cotação e planos de seguro
├── sobre.html                     Institucional
├── login.html / cadastro.html     Autenticação
├── perfil.html / alterar-senha.html   Conta do usuário
├── vendedor-dashboard.html        Painel do vendedor
├── vendedor-veiculos.html         Meus veículos (vendedor/empresa)
├── vendedor-veiculo-form.html     Cadastro/edição de veículo + upload de fotos
├── vendedor-leads.html            Leads recebidos
├── empresa-cadastro.html          Dados da empresa + endereço
├── empresa-verificacao.html       Documentos e selo de confiança
├── empresa-dashboard.html         Painel da empresa
├── comprador-interesses.html      Interesses/favoritos enviados
├── comprador-cotacoes.html        Cotações de seguro do comprador
├── comprador-compras.html         Histórico de compras
├── admin-dashboard.html           Painel administrativo
├── admin-moderacao.html           Fila de moderação de anúncios
├── admin-empresas.html            Verificação/selo de empresas
├── admin-usuarios.html            Gestão de usuários
├── admin-vendas.html              Histórico de vendas da plataforma
│
├── assets/
│   ├── css/style.css              Design system completo (cores, componentes)
│   └── js/app.js                  Interações (menu mobile, galeria, upload, tabs)
│
└── pages/                         Scripts Python que GERAM cada HTML acima
    ├── build_index.py
    ├── build_catalogo.py
    ├── build_veiculo_detalhes.py
    ├── build_empresas.py
    ├── build_servicos_seguros_sobre.py
    ├── build_conta.py
    ├── build_vendedor.py
    ├── build_empresa_dash.py
    ├── build_comprador.py
    └── build_admin.py
```

Os arquivos `icons.py`, `illustrations.py` e `partials.py` (na raiz) são
compartilhados pelos scripts em `pages/`: contêm os ícones SVG, as
ilustrações originais de veículos/skyline e os componentes reutilizáveis
(navbar, rodapé, sidebar dos painéis). Isso mantém todas as telas
consistentes — para mudar a navbar ou o rodapé em todo o site, basta editar
`partials.py` e rodar os scripts novamente:

```bash
cd pages
python3 build_index.py
python3 build_catalogo.py
# ...ou rode todos:
for f in *.py; do python3 "$f"; done
```

## Sobre as imagens
Não usei fotos de banco de imagens (evita problemas de licenciamento). Em
vez disso, criei ilustrações SVG originais no mesmo estilo visual da
referência (carro estilizado + skyline de Palmas em navy/verde). Elas são
geradas por código em `illustrations.py`, então são leves, nítidas em
qualquer resolução e fáceis de trocar por fotos reais depois — basta
substituir a chamada `car_card_illustration(...)` por uma tag `<img>`
apontando para a foto real do veículo.

## Próximos passos sugeridos
- Trocar os dados de exemplo (veículos, empresas, usuários) por dados reais
  vindos do backend Django descrito na documentação.
- Se for usar como templates Django, mover `navbar()`, `footer()` etc. de
  `partials.py` para `{% include %}` e os HTMLs para `templates/`.
- Ajustar `assets/js/app.js` para os endpoints reais (upload de fotos,
  favoritos, filtros do catálogo).
