import os.path
import json

def get_config():
    config_file = os.path.join('cfg', 'config.json')
    with open(config_file) as f:
        config = json.load(f)
        return config

if __name__ == '__main__':
    config = get_config()
