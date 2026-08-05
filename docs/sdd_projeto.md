# Software Design Document (SDD)

# IronSistemaDeInspecao

Versão: 0.1

---

                                 IronSistemaDeInspecao

                                   Empresa (Tenant)

                                                │

                                        Banco dedicado por empresa

                                                │

                                        Contexto do Tenant

                                                │

                                        Database Router Django

                                                │

                                        Pipeline Inteligente

                                                │

                                ┌──────────────┼──────────────┐
                                ▼              ▼              ▼

                                Detector      Classificador    Eventos

                                ▼              ▼              ▼

                                        ItemInspecionado

                                                │

                                        Motor de Regras

                                                │

                                        PostgreSQL Operacional

                                                │

                                        Banco Vetorial

                                                │

                                        Dashboard

# 1. Objetivo

O IronSistemaDeInspecao é uma plataforma de inspeção industrial baseada em Inteligência Artificial destinada à classificação automática de produtos em esteiras.

A plataforma deve ser independente do produto inspecionado, permitindo reutilização para diferentes segmentos industriais, como:

- Abacaxi
- Tomate
- Laranja
- Maçã
- Batata
- Garrafas
- Peças industriais
- Qualquer objeto detectável por modelos de Visão Computacional.

A IA é responsável por identificar características do objeto.

As decisões operacionais são responsabilidade do motor de regras.

---

# 2. Objetivos Técnicos

- Arquitetura modular.
- Arquitetura orientada a eventos.
- Separação completa entre IA e regras de negócio.
- Componentes desacoplados.
- Facilidade para adicionar novos modelos.
- Facilidade para adicionar novos produtos.
- Total rastreabilidade das decisões.
- Aprendizado contínuo através do histórico operacional.

---

# 3. Arquitetura Geral

Fluxo principal

Captura da imagem

↓

Detecção

↓

Classificações

↓

Motor de Regras

↓

Destino

↓

Persistência

↓

Vetorização

↓

Eventos

↓

Relatórios

---

# 4. Componentes

## Detector

Responsável por localizar objetos na imagem.

Entrada

Imagem

Saída

ItemInspecionado

Tecnologias

- YOLO
- RT-DETR
- Grounding DINO
- Outros modelos futuros

---

## Classificadores

Responsáveis por enriquecer o ItemInspecionado.

Exemplos

- Qualidade
- Defeitos
- Tamanho
- Peso
- Cor
- Maturação
- Tipo
- Outros classificadores futuros

Cada classificador deve ser independente.

---

## Motor de Regras

Responsável por decidir:

- destino
- linha
- prioridade
- descarte
- exportação
- processamento
- consumo

O motor de regras nunca executa IA.

Ele apenas utiliza as informações produzidas pelos classificadores.

---

## Serviço de Conhecimento

Responsável por:

- gerar embeddings
- consultar embeddings
- construir contexto
- responder perguntas
- alimentar a base vetorial

---

## Persistência

Dois bancos PostgreSQL independentes.

### Banco Operacional

Responsável pelos dados estruturados.

Armazena:

- Produtos
- Itens
- Inspeções
- Eventos
- Regras
- Usuários
- Configurações
- Relatórios

---

### Banco Vetorial

Responsável apenas pela memória semântica.

Armazena:

- Embeddings
- Documento textual
- Metadados
- Imagens
- Versão do modelo
- Produto

Utilizar extensão pgvector.

---

# 5. Pipeline

Imagem

↓

ServiçoDeteccao

↓

ItemInspecionado

↓

ServiçoQualidade

↓

ServiçoDefeitos

↓

ServiçoTipo

↓

ServiçoTamanho

↓

ServiçoPeso

↓

ServiçoDestino

↓

Persistência

↓

Vetorização

↓

Publicação de Eventos

---

# 6. Arquitetura Orientada a Eventos

Eventos previstos

- ImagemRecebida
- ObjetoDetectado
- QualidadeClassificada
- DefeitosIdentificados
- TipoClassificado
- PesoEstimado
- TamanhoCalculado
- DestinoCalculado
- ItemPersistido
- EmbeddingGerado
- DocumentoVetorizado
- ItemFinalizado

Novos eventos poderão ser adicionados sem alterar o pipeline existente.

---

# 7. Rastreabilidade

Cada ItemInspecionado possuirá um histórico completo.

Exemplo

- horário da captura
- horário da detecção
- horário das classificações
- modelo utilizado
- versão do modelo
- operador
- destino
- tempo de processamento
- decisão tomada
- motivo da decisão

Nenhuma informação será descartada.

---

# 8. Aprendizado Contínuo

Toda correção realizada por um operador será registrada.

Serão armazenados:

- decisão da IA
- decisão humana
- motivo da alteração
- imagem
- embeddings
- versão dos modelos
- data e hora

Esses registros poderão ser utilizados futuramente para treinamento de novos modelos.

---

# 9. Relatórios

A plataforma deverá gerar automaticamente:

Operacionais

- Produção diária
- Produção semanal
- Produção mensal
- Tempo médio de inspeção
- Quantidade por linha
- Quantidade por qualidade
- Quantidade por defeito
- Quantidade por produto

Gerenciais

- Eficiência dos modelos
- Histórico de correções
- Distribuição de defeitos
- Produtos descartados
- Taxa de aprovação
- Comparativos por período

---

# 10. Escalabilidade

A plataforma deve permitir:

- adicionar novos produtos
- adicionar novos modelos
- adicionar novos classificadores
- alterar regras sem reprocessar modelos
- utilizar diferentes modelos simultaneamente
- integrar CLPs
- integrar esteiras industriais
- integrar ERPs
- integrar dashboards em tempo real

Sem necessidade de reestruturação da arquitetura.

---

# 11. Princípios Arquiteturais

- Domain-Driven Design (DDD)
- Arquitetura Orientada a Eventos (EDA)
- Responsabilidade Única (SRP)
- Baixo Acoplamento
- Alta Coesão
- Serviços Independentes
- IA desacoplada das regras de negócio
- Persistência separada da camada de inteligência
- Base vetorial independente do banco operacional
- Pipeline extensível por plugins

a partir do monorepo, cada componente será um projeto separado.

ironSistemaDeInspecao/

├── backend/ # Django
├── ia/ # Modelos e pipelines
├── agentes/ # Futuros agentes de IA
├── dashboard/ # React ou Django Templates
├── app-mobile/ # React Native (futuro)
├── docs/
│ ├── 000-visao.md
│ ├── 001-sdd.md
│ ├── 002-ddd.md
│ ├── 003-eventos.md
│ ├── 004-arquitetura.md
│ ├── 005-api.md
│ └── adr/ # Architecture Decision Records
├── docker/
└── docker-compose.yml

dominio geral

Empresa
│
├── Produtos
├── Esteiras
├── Câmeras
├── Workflows
├── Modelos
└── Usuários

Captura
│
├── Imagem
├── Timestamp
├── Câmara
└── Itens

ItemInspecionado
│
├── BoundingBox
├── Qualidade
├── Defeitos
├── Peso
├── Tipo
├── Destino
└── Eventos

Conhecimento
│
├── Documento
├── Embedding
├── Similaridades
└── Feedback

Workflow
│
├── Etapas
├── Execuções
└── Resultados

Isso nos permite:

rastrear exatamente de qual captura cada item veio;
armazenar a imagem original apenas uma vez;
reprocessar uma captura inteira com um modelo novo;
comparar resultados entre versões de modelos;
gerar datasets automaticamente a partir das capturas.


iron-sistema-de-inspecao/
│
├── agentes/
│
├── app-mobile/
│
├── backend/
│   ├── apps/
│   │
│   ├── config/
│   │   ├── settings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   └── production.py
│   │   │
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   ├── wsgi.py
│   │   └── __init__.py
│   │
│   ├── core/
│   │   ├── domain/
│   │   ├── application/
│   │   ├── infrastructure/
│   │   ├── shared/
│   │   └── __init__.py
│   │
│   ├── tests/
│   │
│   ├── requirements/
│   │   ├── base.txt
│   │   ├── development.txt
│   │   └── production.txt
│   │
│   ├── manage.py
│   └── .env
│
├── docker/
│   │
│   ├── backend/
│   │   ├── Dockerfile
│   │   └── entrypoint.sh
│   │
│   ├── postgres/
│   │
│   ├── postgres-ai/
│   │
│   ├── redis/
│   │
│   └── minio/
│
├── docs/
│   │
│   ├── 00-visao.md
│   ├── 01-sdd.md
│   ├── 02-roadmap.md
│   │
│   ├── adr/
│   │
│   ├── ddd/
│   │
│   └── sprints/
│       └── sprint-001/
│           ├── README.md
│           ├── checklist.md
│           ├── decisoes.md
│           └── retrospectiva.md
│
├── scripts/
│
├── .editorconfig
├── .gitignore
├── .env.example
├── docker-compose.yml
├── Makefile
├── README.md
└── LICENSE