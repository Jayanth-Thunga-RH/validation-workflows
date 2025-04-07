import json
import os
import sys

PROJECT_JSON = "project.json"
APPROVED_DEPENDENCIES_JSON = ".infra/scripts/.approved-dependencies.json"

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    if not os.path.exists(PROJECT_JSON):
        print(f"ERROR: {PROJECT_JSON} not found.")
        sys.exit(1)

    if not os.path.exists(APPROVED_DEPENDENCIES_JSON):
        print(f"ERROR: {APPROVED_DEPENDENCIES_JSON} not found.")
        sys.exit(1)

    project_data = load_json(PROJECT_JSON)
    approved_data = load_json(APPROVED_DEPENDENCIES_JSON)

    project_deps = project_data.get("dependencies", {})

    print("🔍 Validating dependencies...\n")

    has_warnings = False

    for dep, version in project_deps.items():
        approved_version = approved_data.get(dep)
        if approved_version is None:
            print(f"::warning file=project.json::'{dep}' is not in the approved list.")
            has_warnings = True
        elif version != approved_version:
            print(f"::warning file=project.json::'{dep}' version mismatch: found {version}, expected {approved_version}.")
            has_warnings = True

    if not has_warnings:
        print("\n✅ All dependencies match approved versions.")
        sys.exit(0)
    else:
        print("\n⚠️  Dependency issues found. Please review.")
        sys.exit(2)

if __name__ == "__main__":
    main()
