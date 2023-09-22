import os
import json
data = json.load(open('data.json', 'rb'))

import base64
base64String = data['body'] #"JVBERi0xLjQKJeHp69MKMSAwIG9iago8PC9Qcm9kdWNlciAoU2tpYS9..." # ""中为pdf的base64码

with open('temp.pdf', 'wb') as f:
    f.write(base64.b64decode(base64String))

