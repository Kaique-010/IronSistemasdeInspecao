A primeira decisão arquitetural (ADR-0001)
O Iron será um Monólito Modular

Não começaremos com microsserviços.

┌─────────────────────────────────────────────┐
│ Django (Monólito Modular) │
│ │
│ Produtos │
│ Inspeções │
│ Eventos │
│ Workflow │
│ IA │
│ Conhecimento │
│ Relatórios │
│ API │
└─────────────────────────────────────────────┘

Por quê?

Porque:

desenvolvimento mais rápido;
deploy mais simples;
debug muito mais fácil;
transações consistentes;
um único código.

Se um dia precisarmos, extraímos módulos para microsserviços.

ADR-0002
O banco operacional será Multi-Tenant por Banco
PostgreSQL

iron_master

↓

empresa_a

empresa_b

empresa_c

empresa_d

Cada cliente possui seu banco.

Exatamente como o SPSWeb.

ADR-0003
Banco vetorial único
postgres_vector

↓

embeddings

Toda consulta obrigatoriamente filtra

tenant_id
ADR-0004
Event Sourcing Parcial

Essa é uma decisão importante.

Não vamos usar Event Sourcing para tudo.

Só para o domínio de inspeção.

Exemplo

ItemInspecionado

↓

Evento

↓

Evento

↓

Evento

↓

Evento

Mas usuários, empresas, configurações continuam CRUD tradicional.

Isso reduz bastante a complexidade.

ADR-0005
CQRS Parcial

Escrita

↓

Eventos

Leitura

↓

Views otimizadas

Exemplo

Tabela

item_inspecionado

gera

relatorio_diario

gera

dashboard
ADR-0006
Workflow Configurável

Nada ficará fixo.

Workflow

↓

Etapas

↓

Service

Exemplo

Detectar

↓

Qualidade

↓

Defeitos

↓

Destino

Outro

Detectar

↓

OCR

↓

Destino
ADR-0007
Todo Service implementa a mesma interface

Exemplo

class ServicoWorkflow:

    def executar(self, contexto):
        ...

Não importa se é:

YOLO
OCR
Peso
Defeito
Embedding

Todos seguem o mesmo contrato.

ADR-0008
O objeto Contexto

Aqui está a maior mudança que eu faria em relação ao que conversamos.

Até agora falamos do ItemInspecionado.

Mas acho que ele não é suficiente.

Eu criaria um objeto chamado:

ContextoInspecao

Ele vive apenas durante o processamento.

Exemplo:

ContextoInspecao

↓

Frame

↓

Imagem

↓

Item

↓

Eventos

↓

Resultados

↓

Configuração

↓

Tenant

↓

Workflow

↓

Tempo

↓

Modelos

Todos os services recebem exatamente esse objeto.

Nunca recebem parâmetros soltos.

Exemplo

class ServicoPeso:

    def executar(contexto):
        ...

Ele pode acessar

contexto.item
contexto.imagem
contexto.workflow
contexto.tenant
contexto.modelo

Sem precisar mudar assinatura de métodos no futuro.

ADR-0009
Plugins

Tudo é plugin.

DetectorPlugin

ClassificadorPlugin

DestinoPlugin

EmbeddingPlugin

RelatorioPlugin

IntegracaoPlugin
ADR-0010
O Workflow nunca conhece Services

Essa é a parte mais elegante.

O Workflow conhece apenas o nome da etapa.

Exemplo

detectar

O sistema procura

ServicoDeteccao

automaticamente.

Ou seja

Registry.

RegistroServices

↓

"detectar"

↓

ServicoDeteccao

Isso significa que amanhã podemos instalar um plugin novo.

Ele se registra.

E o Workflow passa a enxergá-lo.

Sem alterar uma linha do núcleo.

E aqui vem uma ideia que eu acho que pode ser o coração do Iron

Ao invés de chamar isso de Workflow, eu chamaria de:

Pipeline Inteligente

Porque ele não é um BPM.

Ele é um pipeline que pode conter:

IA
regras
integrações
consultas
embeddings
OCR
APIs externas

Tudo na mesma estrutura.

A partir daqui, eu faria o projeto como uma empresa faz

A próxima etapa não seria escrever código.

Seria criar uma pasta docs/adr/ com as decisões arquiteturais (como as ADRs acima) e uma pasta docs/ddd/ contendo:

Linguagem Ubíqua.
Glossário do domínio.
Contextos Delimitados.
Agregados.
Entidades.
Objetos de Valor.
Eventos de Domínio.
Casos de Uso.
Diagramas do Pipeline Inteligente.
