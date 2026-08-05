Sprint 0002 — DDD e Domínio

Objetivo: transformar o documento em código.

Linguagem Ubíqua
Contextos Delimitados
Agregados
Entidades
Value Objects
Eventos de Domínio
Casos de Uso
ADRs
Registry de plugins
ContextoInspecao

Entrega:

docs/
ddd/
adr/
core/domain/
Sprint 0003 — Produtos e Configuração

Primeiro domínio real.

Empresa
├── Produto
├── Linha
├── Camera
├── Workflow

Models

Produto
Linha
Camera
Workflow
ModeloIA

Admin

API

CRUD completo

Sprint 0004 — Captura de Imagens

Primeira integração com visão.

Imagem

↓

Upload

↓

MinIO

↓

Registro

Model

Captura

Campos

empresa
camera
arquivo
hash
timestamp
status

Entrega

Upload
Salvar no MinIO
Persistir banco
Sprint 0005 — Detector (YOLO)

Primeira IA.

Imagem

↓

YOLO

↓

Bounding Boxes

Criar

DetectorPlugin

Interface

class DetectorPlugin:

    def detectar(self, contexto):
        ...

Implementação

YOLODetector

Resultado

ItemInspecionado
Sprint 0006 — Pipeline Inteligente

O coração do Iron.

Criar

ContextoInspecao

Criar

PipelineExecutor

Exemplo

Captura

↓

Detector

↓

Qualidade

↓

Destino

↓

Persistência
Sprint 0007 — Registry de Plugins

Nada conhece nada.

registry.py
registry.register(
"detector",
YOLODetector
)

Depois

plugin = registry.get("detector")
Sprint 0008 — Eventos

Criar Event Bus interno.

Eventos

ImagemRecebida

ObjetoDetectado

DestinoCalculado

ItemPersistido
Sprint 0009 — Classificadores

Cada um independente.

ServicoQualidade

ServicoPeso

ServicoCor

ServicoDefeito

ServicoTipo

Todos implementam

executar(contexto)
Sprint 0010 — Motor de Regras

Recebe apenas

ContextoInspecao

Nunca chama IA.

Somente decide.

Destino

Linha

Descarte

Prioridade
Sprint 0011 — Banco Vetorial

Criar

Documento

Embedding

Consulta

Memória

Integração

pgvector
Sprint 0012 — RAG

Criar

KnowledgeService

Fluxo

Pergunta

↓

Busca Vetorial

↓

LLM

↓

Resposta
Sprint 0013 — Dashboard

Primeiro painel.

Produção

Tempo

Defeitos

Qualidade

Eventos
Sprint 0014 — Tempo Real
WebSocket

Redis

Eventos

Dashboard
Sprint 0015 — Auditoria

Tudo rastreável.

Quem

Quando

Modelo

Versão

Imagem

Resultado

Correção Humana
Sprint 0016 — Treinamento

Gerar datasets automaticamente.

Imagem

Bounding Box

Classe

Correção

↓

Dataset
Sprint 0017 — Produção
Docker otimizado
Nginx
Gunicorn
Celery
Monitoramento
Logs
Backup
Health Checks
Observabilidade
Visão geral
0001 ✅ Fundação Multi-tenant
0002 ✅ DDD e Domínio
0003 ✅ Produtos e Configuração
0004 Captura
0005 YOLO
0006 Pipeline
0007 Plugins
0008 Eventos
0009 Classificadores
0010 Motor de Regras
0011 Vetores
0012 RAG
0013 Dashboard
0014 Tempo Real
0015 Auditoria
0016 Aprendizado Contínuo
0017 Produção

Sprint Tempo
0002 - DDD + Documentação 1 dia
0003 - Produtos 1 dia
0004 - Captura + MinIO 1 dia
0005 - YOLO 2 dias
0006 - Pipeline Inteligente 2 dias
0007 - Plugins 1 dia
0008 - Event Bus 1 dia
0009 - Classificadores 2 dias
0010 - Motor de Regras 2 dias
0011 - pgvector 1 dia
0012 - RAG 2 dias
0013 - Dashboard 2 dias
0014 - WebSocket 1 dia
0015 - Auditoria 1 dia
0016 - Aprendizado Contínuo 2 dias
0017 - Produção 2 dias

total 10 dias

Hoje a arquitetura já suporta:

✅ Multi-tenant por banco
✅ Banco vetorial
✅ RAG
✅ Pipeline
✅ Plugins
✅ Event Bus
✅ IA desacoplada
✅ Workflows configuráveis
✅ Auditoria
✅ Aprendizado contínuo

2 sprint por dia, em média.
Sprints maiores (YOLO, Pipeline, RAG) podem consumir mais

Cada sprint tem uma pasta em docs/sprints.
Cada sprint gera commits pequenos e organizados.
Cada sprint termina com:
testes passando;
documentação atualizada;
