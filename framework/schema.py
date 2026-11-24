"""
Spec helpers: load an OpenAPI file (YAML or JSON) and validate payloads against its schemas.

    spec = load_spec("openapi.yaml")
    assert_matches_schema(body, "Charger", spec)          # by component name
    assert_matches_schema(body, {"type": "object"})        # or an inline JSON Schema

If the spec is prose (Markdown/PDF), write the schema inline as a dict instead.
"""
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker


def load_spec(path: str | Path) -> dict:
    text = Path(path).read_text(encoding="utf-8")
    if str(path).endswith(".json"):
        return json.loads(text)
    return yaml.safe_load(text)


def _schema_for(schema: str | dict, spec: dict | None) -> dict:
    if isinstance(schema, dict):
        return schema
    if spec is None:
        raise ValueError(f"A spec is needed to look up the schema named '{schema}'")
    if schema not in spec.get("components", {}).get("schemas", {}):
        raise KeyError(f"Schema '{schema}' not found under components.schemas in the spec")
    # Embed components so internal $refs (#/components/schemas/...) resolve.
    return {"$ref": f"#/components/schemas/{schema}", "components": spec["components"]}


def schema_errors(instance, schema: str | dict, spec: dict | None = None) -> list[str]:
    validator = Draft202012Validator(_schema_for(schema, spec), format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path))
    return [f"{'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}" for e in errors]


def assert_matches_schema(instance, schema: str | dict, spec: dict | None = None):
    errors = schema_errors(instance, schema, spec)
    assert not errors, "Response does not match the spec:\n  - " + "\n  - ".join(errors) + \
        f"\nBody: {json.dumps(instance, indent=2)[:1500]}"
