from pathlib import Path


def get_scripts(path: Path) -> list[Path]:
    s: list[Path] = []
    if not path.exists() or not path.is_dir():
        return []

    for file in path.glob('*.py'):
        if file.name != '__init__.py':
            s.append(file)

    return s
