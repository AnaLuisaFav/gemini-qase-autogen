import os
import re
import sys
import json
import requests
import google.generativeai as genai

from dotenv import load_dotenv
from qase.prompt import build_prompt
from qase.utils import get_or_create_suite_id
from qase.payload_builder import build_case_payload

load_dotenv(override=True)

# === CONFIG ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QASE_API_TOKEN = os.getenv("QASE_API_TOKEN")
QASE_PROJECT_CODE = os.getenv("QASE_PROJECT_CODE")

HEADERS = {
    "Content-Type": "application/json",
    "Token": QASE_API_TOKEN
}

# === Inicia Gemini ===
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')

# === Input do requisito ===
print("📥 Cole abaixo o nome da suíte + os requisitos (pressione Ctrl+Z + Enter no Windows ou Ctrl+D no Linux/macOS):\n")

"""
Exemplo de entrada:
Autenticação de Usuário 
1. O usuário deve ser capaz de se autenticar com sucesso usando um nome de usuário e senha válidos.
2. O sistema deve rejeitar tentativas de autenticação com credenciais inválidas.
"""

requisito = sys.stdin.read().strip()

# === Gera nome da suíte a partir da primeira linha do requisito ===
suite_name = requisito.splitlines()[0].strip()[:80] 

# === Cria a suíte (ou obtém se já existir)
suite_id = get_or_create_suite_id(QASE_PROJECT_CODE, suite_name, HEADERS)

if suite_id is None:
    print("❌ Não foi possível obter ou criar a suíte. Encerrando.")
    exit(1)

# === Prompt para geração
prompt = build_prompt(requisito)

# === Gera resposta do Gemini
response = model.generate_content(prompt)
raw_json = response.text.strip()
raw_json = re.sub(r"^```json\n?|```$", "", raw_json.strip(), flags=re.MULTILINE)

try:
    generated_cases = json.loads(raw_json)
except json.JSONDecodeError:
    print("❌ Erro ao converter a resposta do Gemini para JSON:")
    print(raw_json)
    exit(1)

# === Envia cada caso para o Qase
print(f"\n📤 Enviando {len(generated_cases)} caso(s) de teste para o Qase - Projeto: ({QASE_PROJECT_CODE})\n")

for case in generated_cases:
    payload = build_case_payload(case, suite_id)

    res = requests.post(
        f"https://api.qase.io/v1/case/{QASE_PROJECT_CODE}",
        headers=HEADERS,
        json=payload
    )

    if res.status_code in [200, 201]:
        print(f"✅ Caso enviado: {case['title']}")
    else:
        print(f"❌ Erro ao enviar '{case['title']}': {res.status_code} - {res.text}")

print("\n🏁 Finalizado.")
