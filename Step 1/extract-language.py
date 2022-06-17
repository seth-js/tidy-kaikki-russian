import json
import fileinput

lang = "Russian"

output = []

for line in fileinput.input(
    "raw-wiktextract-data.json", openhook=fileinput.hook_encoded("utf-8")
):
    if f'"lang": "{lang}"' in line:
        output.append(line.strip())

json_file = []

for entry in output:
    json_file.append(json.loads(entry))

print(f"Writing {lang.lower()}-wikiextract.json...")

with open(f"{lang.lower()}-wikiextract.json", "w", encoding="utf-8") as f:
    json.dump(json_file, f)

print("Finished.")
