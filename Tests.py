import yaml

filepath = "material_repository/basalGanglia.yaml"

try:
    with open(filepath, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
        print("✅ Successfully loaded:", data)
except yaml.YAMLError as e:
    print("❌ YAML Error:", e)
except Exception as e:
    print("❌ Other Error:", e)
