import os
import re
import sys
import json
import requests
import google.generativeai as genai

from dotenv import load_dotenv
from qase.prompt import build_prompt
from qase.utils import get_mapped_value, list_to_text
from qase.payload_builder import build_case_payload

# === CONFIG ===
load_dotenv(override=True)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QASE_API_TOKEN = os.getenv("QASE_API_TOKEN")
QASE_PROJECT_CODE = os.getenv("QASE_PROJECT_CODE")

# === Inicia Gemini ===
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')

# === Input do requisito ===
print("📥 Cole abaixo os requisitos (pressione Ctrl+Z + Enter no Windows ou Ctrl+D no Linux/macOS):\n")
requisito = sys.stdin.read().strip()

# === Prompt para geração ===
prompt = build_prompt(requisito)

# === Gera resposta do Gemini ===
response = model.generate_content(prompt)
raw_json = response.text.strip()
raw_json = re.sub(r"^```json\n?|```$", "", raw_json.strip(), flags=re.MULTILINE)

try:
    generated_cases = json.loads(raw_json)
except json.JSONDecodeError:
    print("❌ Erro ao converter a resposta do Gemini para JSON:")
    print(raw_json)
    exit(1)

HEADERS = {
    "Content-Type": "application/json",
    "Token": QASE_API_TOKEN
}

print(f"\n📤 Enviando {len(generated_cases)} caso(s) para o Qase ({QASE_PROJECT_CODE})...\n")

# === Envia cada caso
for case in generated_cases:
    payload = build_case_payload(case)

    print("\n📦 Enviando o seguinte payload:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))

    res = requests.post(
        f"https://api.qase.io/v1/case/{QASE_PROJECT_CODE}",
        headers=HEADERS,
        json=payload
    )

    if res.status_code == 200:
        print(f"✅ Caso enviado: {case['title']}")
    else:
        print(f"❌ Erro ao enviar '{case['title']}': {res.status_code} - {res.text}")

print("\n🏁 Finalizado.")
