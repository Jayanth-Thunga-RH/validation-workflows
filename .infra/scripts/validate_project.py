import json
import os
import sys

# Use path relative to the script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../"))
PROJECT_JSON = os.path.join(ROOT_DIR, "project.json")
APPROVED_DEPENDENCIES_JSON = os.path.join(SCRIPT_DIR, ".approved-dependencies.json")

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    # Load project.json
    if not os.path.exists(PROJECT_JSON):
        print(f"ERROR: {PROJECT_JSON} not found.")
        sys.exit(1)

    project_data = load_json(PROJECT_JSON)
    project_deps = project_data.get("dependencies", {})

    # Load approved dependencies
    if not os.path.exists(APPROVED_DEPENDENCIES_JSON):
        print(f"ERROR: {APPROVED_DEPENDENCIES_JSON} not found.")
        sys.exit(1)

    approved_data = load_json(APPROVED_DEPENDENCIES_JSON)

    # Validate
    print("🔍 Validating dependencies...\n")
    has_warnings = False

    for dep, version in project_deps.items():
        approved_version = approved_data.get(dep)
        if approved_version is None:
            print(f"WARNING: '{dep}' is not in the approved list.")
            has_warnings = True
        elif version != approved_version:
            print(f"WARNING: '{dep}' version mismatch. Project has {version}, expected {approved_version}.")
            has_warnings = True

    if not has_warnings:
        print("✅ All dependencies match approved versions.")
    else:
        print("\n⚠️ Dependency warnings found. Please review before merging.")

if __name__ == "__main__":
    main()
