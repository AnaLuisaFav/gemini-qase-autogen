import requests

def get_mapped_value(field, value, mapping, default):
    key = value.lower().strip() if value else ""
    if key not in mapping:
        print(f"⚠️  Valor inválido para '{field}': '{value}' → Usando default '{default}'")
        return mapping[default]
    return mapping[key]

def list_to_text(value):
    if isinstance(value, list):
        return "\n".join(value)
    return value or ""

def get_or_create_suite_id(project_code, suite_name, headers):
    print(f"🔍 Buscando suíte com nome '{suite_name}'...")

    res = requests.get(
        f"https://api.qase.io/v1/suite/{project_code}",
        headers=headers
    )

    if res.status_code != 200:
        print(f"❌ Erro ao buscar suítes: {res.status_code} - {res.text}")
        return None

    suites = res.json().get("result", {}).get("entities", [])
    for suite in suites:
        if suite["title"].strip().lower() == suite_name.lower():
            print(f"✅ Suíte encontrada (ID: {suite['id']})")
            return suite["id"]

    print("🆕 Suíte não encontrada. Criando nova...")

    res_create = requests.post(
        f"https://api.qase.io/v1/suite/{project_code}",
        headers=headers,
        json={"title": suite_name}
    )

    if res_create.status_code == 200:
        suite_id = res_create.json()["result"]["id"]
        print(f"✅ Suíte criada com sucesso (ID: {suite_id})")
        return suite_id
    else:
        print(f"❌ Erro ao criar suíte: {res_create.status_code} - {res_create.text}")
        return None
