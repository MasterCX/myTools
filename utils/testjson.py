import json
import os

with open('test.json', 'r+') as f:
    jobj = json.load(f)
    for shape in jobj['shapes']:
        if shape['label'] == 'xx':
            shape.update({"label": "bb"})
    with open('test1.json', 'w') as fw:
        json.dump(jobj, fw)
