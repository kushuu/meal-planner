import yaml


def get_settings():
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    return config