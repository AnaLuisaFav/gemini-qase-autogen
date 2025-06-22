def build_prompt(requisito: str) -> str:
    return f"""
Como um especialista em testes de software, crie casos de teste completos com base nos seguintes requisitos:

{requisito}

A resposta deve ser um array JSON com objetos no formato a seguir:

- nome da suíte
- title
- description
- preconditions
- postconditions
- priority: low | medium | high
- severity: trivial | minor | major | critical | blocker
- type: other | functional | regression | performance | usability | security
- behavior: positive | negative | destructive
- automation: is-automated | is-not-automated
- steps_type: classic
- layer: e2e | api | unit
- steps: lista de objetos com:
  - position
  - action
  - expected_result

Use uma estrutura clara e objetiva. Gere múltiplos casos, cobrindo cenários positivos, negativos, limites e alternativos. Aplique técnicas de teste como equivalência, limite, decisão e estado.
Não inclua comentários ou explicações fora do JSON.
""".strip()
