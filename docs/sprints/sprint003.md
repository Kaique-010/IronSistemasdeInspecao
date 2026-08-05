# Sprint 0003 — Produtos e Configuração

## Objetivo

Primeiro domínio real da plataforma: cadastro de produtos, linhas (esteiras), câmeras, workflows (com etapas) e modelos de IA.

## Entrega

✅ Apps separados por contexto:

- `apps.produtos` → Produto
- `apps.configuracao` → Linha, Camera, Workflow, Etapa
- `apps.ia` → ModeloIA

## Models

### Produto (apps.produtos)

- `nome`, `codigo` (SKU, único), `descricao`, `categoria`, `ativo`, timestamps

### Linha (apps.configuracao)

- `nome`, `codigo` (único), `descricao`, `produto` (FK opcional → Produto), `ativo`

### Camera (apps.configuracao)

- `nome`, `identificador` (IP/URL), `tipo` (IP/USB/Stream), `linha` (FK → Linha), `ativo`

### Workflow (apps.configuracao)

- `nome`, `descricao`, `produto` (FK → Produto), `ativo`

### Etapa (apps.configuracao)

- `workflow` (FK), `ordem`, `tipo` (detecção/classificação/destino), `ativo`
- Ordenada por `ordem`; `unique_together (workflow, ordem)`

### ModeloIA (apps.ia)

- `nome`, `tipo` (detector/classificador), `versao`, `arquivo`, `descricao`, `ativo`
- `unique_together (nome, versao)`

## Administração

✅ Todos os models registrados no admin do Django

## API (DRF)

✅ Instalado `djangorestframework`
✅ Router único em `/api/`
✅ CRUD completo (viewsets):

- `/api/produtos/`
- `/api/linhas/`
- `/api/cameras/`
- `/api/workflows/` (retorna etapas aninhadas)
- `/api/etapas/`
- `/api/modelos/`

✅ Filtros de busca (`?search=`) e ordenação (`?ordering=`)

## Multi-tenant

✅ Dados gravados no banco da empresa via header `X-Tenant`
✅ Provisionamento do tenant aplica as migrations dos novos apps
✅ Isolamento verificado manualmente (criado produto no tenant, default continua vazio)

## Testes

✅ 18 testes passando:

- Model + API de Produto
- Model + API de Linha/Camera/Workflow/Etapa
- Model + API de ModeloIA
- Router multi-tenant

## Pendências

- Autenticação na API (futuro)
- CRUD de `apps.inspecoes` (Inspecao) não faz parte desta sprint
