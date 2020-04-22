import os
import json

with open(os.path.join('cfg', 'config.json')) as f:
    config = json.load(f)