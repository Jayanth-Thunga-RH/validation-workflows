import json
import os
import sys

PROJECT_JSON = "project.json"
APPROVED_DEPENDENCIES_JSON = os.path.join(os.path.dirname(__file__), ".approved-dependencies.json")

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_version(value):
    # If version is a list like ["2.20.11"], return first item
    if isinstance(value, list):
        return value[0] if value else None
    return value

def main():
    if not os.path.exists(PROJECT_JSON):
        print(f"❌ ERROR: {PROJECT_JSON} not found.")
        sys.exit(1)

    project_data = load_json(PROJECT_JSON)
    project_deps = project_data.get("dependencies", {})

    if not os.path.exists(APPROVED_DEPENDENCIES_JSON):
        print(f"❌ ERROR: {APPROVED_DEPENDENCIES_JSON} not found.")
        sys.exit(1)

    approved_data = load_json(APPROVED_DEPENDENCIES_JSON)

    print("🔍 Validating dependencies...\n")
    has_issues = False

    for dep, version in project_deps.items():
        project_version = normalize_version(version)
        approved_version = normalize_version(approved_data.get(dep))

        if approved_version is None:
            print(f"⚠️  '{dep}' is not in the approved list.")
            has_issues = True
        elif project_version != approved_version:
            print(f"⚠️  '{dep}' version mismatch. Found [{project_version}], expected [{approved_version}].")
            has_issues = True

    if has_issues:
        print("\n⚠️  Dependency issues found. Please review.")
        sys.exit(2)
    else:
        print("✅ All dependencies match approved versions.")

if __name__ == "__main__":
    main()
