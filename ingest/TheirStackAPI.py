import requests
import os
import json
import time
from datetime import datetime, timezone
from dotenv import load_dotenv

from config.job_title_terms import JOB_TITLE_MATCH_TERMS
from transform.job_title_matcher import tag_job_title

load_dotenv()

API_KEY = os.getenv("THEIRSTACK_API_KEY")
BASE_URL = "https://api.theirstack.com/v1/jobs/search"
LIMIT = 20               
MAX_PAGES = 3           
SLEEP_SECONDS = 2     

if not API_KEY:
    raise Exception("API KEY não encontrada.")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

ingestion_timestamp = datetime.now(timezone.utc).isoformat()
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
base_path = f"data/bronze/{today}"
os.makedirs(base_path, exist_ok=True)

page = 0

while page < MAX_PAGES:
    payload = {
        "page": page,
        "limit": LIMIT,
        "job_country_code_or": ["BR"],
        "posted_at_max_age_days": 7,
        "job_title_or": [
            # Data Engineering
            "data engineer",
            "data engineering",
            "engenheiro de dados",
            "big data engineer",
            "engenheiro de big data",

            # Analytics / BI
            "data analyst",
            "data analytics",
            "analista de dados",
            "analytics engineer",
            "engenheiro de analytics",
            "business intelligence",
            "bi analyst",
            "analista de business intelligence",

            # Science / AI
            "data scientist",
            "cientista de dados",
            "machine learning engineer",
            "engenheiro de machine learning",
            "artificial intelligence engineer",
            "engenheiro de inteligência artificial"
        ],
        "job_title_not": [
            "intern",
            "estágio",
            "trainee"
        ]
    }

    response = requests.post(BASE_URL, json=payload, headers=headers)

    # Tratamento explícito de 403 (excesso de requisições)
    if response.status_code in (403, 429):
        print("⏳ Rate limit atingido. Aguardando 5 minutos...")
        time.sleep(300)
        continue

    # Tratamento explícito de 402 (limite do plano excedido ou filtro não permitido)
    if response.status_code == 402:
        print("💳 402 Payment Required — limite do plano atingido ou filtro não permitido.")
        break

    response.raise_for_status()

    raw_data = response.json()

    print(f"Status Code: {response.status_code}")
    print("Chaves do JSON:", raw_data.keys())

    jobs = raw_data.get("data", [])

    for job in jobs:
        job_title = job.get("job_title") or job.get("title")

        match_info = tag_job_title(job_title, JOB_TITLE_MATCH_TERMS)

        job["match_metadata"] = {
            "matched_term": match_info["matched_term"],
            "category": match_info["category"]
        }

    print("Quantidade de jobs:", len(jobs))

    if not jobs:
        print("🔚 Nenhuma vaga retornada. Fim da paginação.")
        break

    bronze_record = {
        "ingestion_metadata": {
            "ingestion_timestamp": ingestion_timestamp,
            "source": "theirstack_api",
            "endpoint": "/v1/jobs/search",
            "page": page,
            "limit": LIMIT
        },
        "data": raw_data
    }

    file_path = f"{base_path}/page_{page}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(bronze_record, f, indent=2, ensure_ascii=False)

    print(f"✅ Página {page} salva ({len(jobs)} vagas)")

    if len(jobs) < LIMIT:
        print("🔚 Última página detectada.")
        break

    page += 1
    time.sleep(SLEEP_SECONDS)

print("📦 Ingestão finalizada.")
