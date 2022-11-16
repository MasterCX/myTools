import json
import os

files = os.listdir('./0906/')
for file in files:
    if file.endswith('.json'):
        with open('./0906/' + file, 'r') as f:
            jobj = json.load(f)
            for shape in jobj['shapes']:
                if shape['label'] == 'biob':
                    shape.update({"label": "blob"})
            with open('./json/' + file, 'w') as fw:
                json.dump(jobj, fw)
