# Vagômetro — Pipeline de Vagas de Dados no Brasil

Projeto de engenharia de dados que coleta, processa e analisa vagas da área de dados no Brasil a partir de uma API externa, utilizando uma arquitetura em camadas (Bronze / Silver / Gold), com controle de custo, ingestão incremental e classificação semântica de cargos.

---

## 🎯 Objetivo

Construir um pipeline de dados realista para:
- Coletar vagas de dados no Brasil
- Controlar consumo de API (créditos)
- Armazenar dados brutos em um data lake
- Processar dados incrementalmente no Databricks
- Permitir análises sobre mercado de trabalho em dados

---

## 🏗️ Arquitetura
-API TheirStack
│
Script Python (coleta e ingestão)
│
Amazon S3 (Bronze layer - JSON)
│
Databricks
│
Delta Lake (Silver/Gold)


---

## 🧱 Camadas do Pipeline

### 🥉 Bronze
- Dados brutos em formato JSON
- Uma página por arquivo
- Particionamento por data
- Metadados de ingestão (timestamp, página, limite)
- Armazenamento no Amazon S3

### 🥈 Silver
- Leitura incremental dos arquivos Bronze
- Normalização dos dados
- Deduplicação por identificador da vaga
- Classificação de cargos por categoria (Data Engineering, Analytics/BI, Data Science/AI)

### 🥇 Gold
- Métricas agregadas, como:
  - Vagas por categoria
  - Vagas por empresa
  - Tendência semanal de vagas
- Base para visualização e análise

---

## 🔎 Classificação de Cargos (Tagging)

Cada vaga é enriquecida com:
- **termo de match**: termo da lista que correspondeu ao título da vaga
- **categoria**: macroárea do cargo

Exemplo:
```json
{
  "job_title": "Senior Data Engineer",
  "match_metadata": {
    "matched_term": "data engineer",
    "category": "data_engineering"
  }
}
```
---
⚙️ Tecnologias Utilizadas

│— Python
│
│— API TheirStack
│
│— Amazon S3
│
│— Databricks
│
│— Delta Lake

---
🚦 Estratégia de Consumo de API

│— Janela de coleta: últimos 7 dias
│
│— Execução: semanal
│
│— Filtro de cargos aplicado na API
│
│— Paginação limitada para controle de custo
│
│— Classificação e refinamento feitos downstream

---
▶️ Execução

│—Executar o script de ingestão localmente
│
│—Os dados são salvos no Amazon S3 (camada Bronze)
│
│—O Databricks consome os dados do S3 para processamento incremental

---
📌 Observações

│—Projeto com foco educacional e de portfólio
│
│—Arquitetura inspirada em pipelines reais de mercado
│
│—Decisões técnicas priorizam clareza, custo e escalabilidade

---
📄 Autor

Marcelo Cabral
