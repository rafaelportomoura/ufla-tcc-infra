import os


def path(group: str, template: str) -> str:
    directory = os.sep.join(os.path.dirname(__file__).split(os.sep)[:-2])
    return os.path.join(directory, "aws", group, template)
