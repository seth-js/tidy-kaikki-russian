import json
import fileinput

print("Reading raw-wiktextract-data.json...")

output = []

for line in fileinput.input(
    "raw-wiktextract-data.json", openhook=fileinput.hook_encoded("utf-8")
):
    if '"lang": "Russian"' in line:
        output.append(line.strip())

print("Finished reading raw-wiktextract-data.json.")

print("Setting up data for ru-wikiextract.json...")

json_file = []

index = 0
for entry in output:
    index += 1
    if index == len(output) or index == 1 or index % 1000 == 0:
        print(f"{index}/{len(output)} entries added...")
    json_file.append(json.loads(entry))

print("Writing ru-wikiextract.json...")

with open("ru-wikiextract.json", "w", encoding="utf-8") as f:
    json.dump(json_file, f)

print("Finished.")
