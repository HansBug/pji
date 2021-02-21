from string import Template


def env_template(template: str, environ=None) -> str:
    return Template(template).substitute(**(environ or {}))
