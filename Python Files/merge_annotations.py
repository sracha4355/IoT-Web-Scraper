import json

##assume all files are in same directory
json_files = ["dom_annotations.json", "chloe_annotation.json", "bharg_annotation.json"]

python_objects = []

for json_file in json_files:
    with open(json_file, "r") as f:
        python_objects.append(json.load(f))

##assume complete_corpus.json already exists in current directory
with open("complete_corpus.json", "w") as f:
    json.dump(python_objects, f, indent=4)