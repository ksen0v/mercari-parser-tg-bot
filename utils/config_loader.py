import json
import os


def load_config() -> json:
    default_config = {
        "bot_token": "token",
        "countdown": 10
    }

    if not os.path.exists('config.json'):
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=4)
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)


config: json = load_config()
BOT_TOKEN: str = config['bot_token']
COUNTDOWN: int = config['countdown']
