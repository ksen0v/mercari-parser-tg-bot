import yaml


def get_yaml(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


texts: dict = get_yaml('texts.yaml')