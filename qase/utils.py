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