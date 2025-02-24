# Módulo Inventário

## Visão Geral
O módulo `inventario` é responsável pelo gerenciamento do inventário de clientes, sites, equipamentos e serviços.

## Estrutura do Módulo
```
inventario/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── cliente.py
│   ├── site.py
│   ├── equipamento.py
│   └── servico.py
├── api/
│   ├── __init__.py
│   ├── views.py
│   ├── urls.py
│   └── serializers.py
└── migrations/
```

## Componentes Principais

### Modelos
1. **Cliente**
   - Vantive ID
   - Razão Social
   - Código
   - Status
   - CNPJ
   
2. **Site**
   - Cliente (FK)
   - CEP
   - Número
   - Complemento
   - Código Sistema Cliente
   - Código Vivo
   - Status
   - Tipo Site
   - Tipo Negócio

3. **Equipamento**
   - Site (FK)
   - Código
   - Status
   - Designador
   - Tipo

4. **Serviço**
   - Equipamento (FK)
   - Código
   - Status
   - Designador
   - Tipo

### Views
1. **ClienteListCreate/Update**
   - Listagem paginada
   - Filtros por razão social, CNPJ, código
   - CRUD completo
   
2. **SiteListCreate/Update**
   - Listagem por cliente
   - Filtros por código e tipo
   - CRUD completo

3. **EquipamentoListCreate/Update**
   - Listagem hierárquica
   - Filtros por site
   - CRUD completo

4. **ServicoListCreate/Update**
   - Listagem hierárquica
   - Filtros por equipamento
   - CRUD completo

### Serializers
1. **ClienteSerializer**
   - Serialização básica do modelo Cliente
   - Todos os campos são expostos

2. **SiteSerializer**
   - Serialização básica do modelo Site
   - Inclui validação de relacionamentos

3. **EquipamentoSerializer**
   - Serialização com dados do Site relacionado
   - Campo calculado site_codigo_vivo

4. **ServicoSerializer**
   - Serialização com dados do Equipamento e Site
   - Campos calculados para códigos relacionados

### Migrations
- Migration inicial (0001_initial)
  - Criação das tabelas principais
  - Definição de relacionamentos
  - Configuração de constraints
  - Índices automáticos

### APIs Disponíveis
- **Clientes**
  - GET/POST `/api/inventario/clientes/`
  - GET/PUT/PATCH/DELETE `/api/inventario/clientes/<id>/`

- **Sites**
  - GET/POST `/api/inventario/sites/`
  - GET/PUT/PATCH/DELETE `/api/inventario/sites/<id>/`

- **Equipamentos**
  - GET/POST `/api/inventario/equipamentos/`
  - GET/PUT/PATCH/DELETE `/api/inventario/equipamentos/<id>/`

- **Serviços**
  - GET/POST `/api/inventario/servicos/`
  - GET/PUT/PATCH/DELETE `/api/inventario/servicos/<id>/`

## Funcionalidades
- Cadastro e gestão de clientes
- Gerenciamento de sites por cliente
- Controle de equipamentos por site
- Gestão de serviços por equipamento
- Histórico de alterações
- Consultas hierárquicas
- Filtros avançados por status e tipo
