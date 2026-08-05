Fundação da plataforma

Objetivo:
Ter uma plataforma pronta para receber domínios.sem regras de negócio

O que entra:

□ Criar repositório

□ Estrutura de pastas

□ Docker Compose

□ Django

□ DRF

□ PostgreSQL Operacional

□ PostgreSQL Vetorial (pgvector)

□ Redis

□ MinIO

□ Variáveis de ambiente

□ Health Check

□ Makefile (ou Taskfile)

□ Pré-commit

□ Ruff

□ Pytest

□ GitHub Actions

                 Docker

        ┌────────────────────┐
        │      Nginx         │
        └─────────┬──────────┘
                  │
        ┌─────────▼──────────┐
        │      Django        │
        └─────────┬──────────┘
                  │
     ┌────────────┼─────────────┐
     │            │             │
     ▼            ▼             ▼

PostgreSQL PostgreSQL Redis
Operacional pgvector
│
▼
MinIO

                 [x] Docker funcionando

Sprint 0001 - Multi Tenant Foundation

[x] Docker base
[x] Infra containers
[x] Configuração .env
[x] Banco operacional
[x] Banco vetorial
[x] Redis
[x] MinIO
[x] Empresa model
[x] Tenant creation service
[x] Tenant context
[x] Tenant middleware
[x] Tenant resolver test
