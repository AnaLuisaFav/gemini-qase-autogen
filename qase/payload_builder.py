from qase.mappings import PRIORITY_MAP, SEVERITY_MAP, TYPE_MAP, BEHAVIOR_MAP, LAYER_MAP
from qase.utils import get_mapped_value, list_to_text

def build_case_payload(case):
    return {
        "title": case["title"][:255],
        "description": list_to_text(case.get("description")),
        "preconditions": list_to_text(case.get("preconditions")),
        "postconditions": list_to_text(case.get("postconditions")),
        "priority": get_mapped_value("priority", case.get("priority"), PRIORITY_MAP, "medium"),
        "severity": get_mapped_value("severity", case.get("severity"), SEVERITY_MAP, "major"),
        "type": get_mapped_value("type", case.get("type"), TYPE_MAP, "functional"),
        "behavior": get_mapped_value("behavior", case.get("behavior"), BEHAVIOR_MAP, "positive"),
        "layer": get_mapped_value("layer", case.get("layer"), LAYER_MAP, "e2e"),
        "is_flaky": 0,
        "steps_type": "classic",
        "steps": [
            {
                "position": step["position"],
                "action": step["action"],
                "expected_result": step["expected_result"]
            } for step in case["steps"]
        ]
    }