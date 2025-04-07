import json
import os
import sys

# Get absolute paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # .infra/scripts
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../"))  # Top level of the repo

PROJECT_JSON = os.path.join(ROOT_DIR, "project.json")
APPROVED_DEPENDENCIES_JSON = os.path.join(SCRIPT_DIR, ".approved-dependencies.json")

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    print(f"🔍 Looking for project.json at: {PROJECT_JSON}")
    print(f"🔍 Looking for approved dependencies at: {APPROVED_DEPENDENCIES_JSON}")

    if not os.path.exists(PROJECT_JSON):
        print(f"❌ ERROR: {PROJECT_JSON} not found.")
        sys.exit(1)

    if not os.path.exists(APPROVED_DEPENDENCIES_JSON):
        print(f"❌ ERROR: {APPROVED_DEPENDENCIES_JSON} not found.")
        sys.exit(1)

    project_data = load_json(PROJECT_JSON)
    approved_data = load_json(APPROVED_DEPENDENCIES_JSON)

    project_deps = project_data.get("dependencies", {})
    has_warnings = False

    print("\n🔎 Validating dependencies...\n")
    for dep, version in project_deps.items():
        approved_version = approved_data.get(dep)
        if approved_version is None:
            print(f"⚠️ WARNING: '{dep}' is not in the approved list.")
            has_warnings = True
        elif version != approved_version:
            print(f"⚠️ WARNING: '{dep}' version mismatch. Project has {version}, expected {approved_version}.")
            has_warnings = True

    if not has_warnings:
        print("✅ All dependencies match approved versions.")
    else:
        print("\n⚠️ Dependency warnings found. Please review before merging.")

if __name__ == "__main__":
    main()
