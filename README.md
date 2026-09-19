======================================================================
MEAT-ESTOQUE-MANAGER (ENTERPRISE WMS & AUDITORIA)
======================================================================
Plataforma de Microsserviços para Gestão de Estoque Perecível, 
Auditoria Transacional e Controle de Lotes (PVPS).

----------------------------------------------------------------------
1. ACESSO ONLINE (LIVE DEMOS)
----------------------------------------------------------------------
- Front-end (UI): https://meat-estoque-manager-nativas.streamlit.app
- Back-end (Docs): https://nativas-grill-estoque-manager.onrender.com/docs
- API Healthcheck: https://nativas-grill-estoque-manager.onrender.com/health

Nota de Infraestrutura: O backend reside no Free Tier do Render. O Cold 
Start pode levar cerca de 50 segundos. Um monitor UptimeRobot pinga a 
rota /health a cada 5 minutos para evitar hibernação.

----------------------------------------------------------------------
2. CONTEXTO OPERACIONAL (O PROBLEMA DE NEGÓCIO)
----------------------------------------------------------------------
O controle de insumos perecíveis (carnes) em churrascarias de alto volume 
gera falhas críticas quando feito em papel: perda de histórico, descarte 
de produtos por validade (falta de PVPS) e falhas de auditoria. 

Este projeto substitui a prancheta física por um Warehouse Management 
System (WMS) digital, transacional e conteinerizado.

----------------------------------------------------------------------
3. DIFERENCIAIS DE ENGENHARIA E REGRAS DE NEGÓCIO
----------------------------------------------------------------------
[A] MOTOR WMS DE LOTES E CASCATA PVPS (FEFO)
O estoque é mapeado em Lotes Físicos (Tabela 'lots'). O backend abate o 
consumo de carne automaticamente dos lotes mais próximos do vencimento 
(ORDER BY expiration_date ASC), garantindo a regra Primeiro que Vence, 
Primeiro que Sai (PVPS) e inativando lotes vazios de forma atômica.

[B] AUDITORIA IMUTÁVEL COM SOFT ROLLBACK (LIFO)
O sistema impede a exclusão física de registros (DELETE) para preservar a 
consistência de dados. A reversão de operações (/reverse) utiliza uma 
pilha LIFO que restaura o saldo e marca o log com a flag booleana 
'is_reversed = True', mantendo a trilha de auditoria forense intacta.

[C] TRATAMENTO DE TIMEZONE EM MÚLTIPLAS CAMADAS
- Persistência: PostgreSQL salva timestamps em UTC (DateTime(timezone=True)).
- Apresentação: Frontend em Streamlit converte o fuso horário para a 
  localidade da operação (America/Cuiaba) utilizando vetorização do Pandas.

[D] CONTROLE DE ACESSO BASEADO EM PAPÉIS (RBAC)
Máquina de estados (st.session_state) no cliente dividindo fluxos:
- Operador: Pesagem de saída e reversão.
- Estoquista: Inventário geral e entrada de lotes novos.
- Administrador: Log forense, indicadores e fechamento de turno.

----------------------------------------------------------------------
4. ARQUITETURA DO SISTEMA (MICROSSERVIÇOS / MONOREPO)
----------------------------------------------------------------------
Desacoplamento total entre Front-end (Dumb Client) e Back-end (REST API):
- Back-end: FastAPI Assíncrono com injeção de dependência e Pydantic.
- Banco de Dados: PostgreSQL isolado com SQLAlchemy 2.0 (ORM).
- Front-end: Streamlit consumindo a API via requests HTTP.
- Infraestrutura: Docker, Docker Compose, DevContainers (GitHub Codespaces).

----------------------------------------------------------------------
5. COMO EXECUTAR O PROJETO LOCALMENTE
----------------------------------------------------------------------
[OPÇÃO A] Nuvem com 1-Click (DevContainers)
O repositório possui devcontainer.json nativo com Docker-in-Docker. Ao 
criar um Codespace, a máquina subirá com Python 3.11, Docker Compose e 
extensões do VS Code pré-instaladas no navegador.

[OPÇÃO B] Deploy Local (Docker Compose)
1. Clone o repositório:
   git clone https://github.com/Rafael-Rodrigues09/Meat-Estoque-Manager.git
   cd Meat-Estoque-Manager

2. Crie um arquivo .env na raiz:
   API_TOKEN=sua_senha_segura
   DATA_PASS=senha_db_postgres
   DATA_URL=postgresql+psycopg2://postgres:${DATA_PASS}@db:5432/postgres
   USER_PASS=senha_frontend
   ADMIN_PASS=senha_historico
   STORAGE_PASS=senha_estoque
   API_URL=http://api:8000

3. Suba a infraestrutura:
   docker compose up --build -d

----------------------------------------------------------------------
6. ENDPOINTS PRINCIPAIS DA API
----------------------------------------------------------------------
- GET /estoque       : Retorna saldo consolidado de carnes.
- POST /add-estoque  : Registra entrada de lotes físicos com validade.
- GET /allestoque    : Lista lotes ativos ordenados por vencimento.
- POST /uso          : Registra consumo e gera histórico em cascata.
- POST /reverse      : Executa rollback atômico (LIFO).
- POST /reset        : Gera backup sanitizado em PDF e zera o turno.
======================================================================