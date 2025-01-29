import os
import importlib.util
from pathlib import Path
import argparse

from src.scripts_utils import get_scripts, import_from_path

scripts_path = Path("scripts")
python_files = get_scripts(scripts_path)
script_names = [f.stem for f in python_files]

def run_main(python_file: Path, *args, **kwargs):
    module = import_from_path(python_file.name, python_file.absolute())
    if not hasattr(module, "main"):
        print("No main found!")
        return

    # Pass args and kwargs to the main function
    module.main(*args, **kwargs)

def run(script_name, args, kwargs):
    """Run a script from the scripts directory with optional args and kwargs"""
    if script_name not in script_names:
        print(f"Script {script_name} not found. Available scripts: {', '.join(script_names)}")
        return

    # Parse kwargs into a dictionary
    kwargs_dict = {key: value for key, value in kwargs.items()}

    run_main(scripts_path / Path(script_name).with_suffix(".py"), *args, **kwargs_dict)

def new(script_name):
    """Create a new script template"""
    scripts_path = Path("scripts")
    scripts_path.mkdir(exist_ok=True)
    with open('resources/template.txt', 'r') as f:
        template = f.read()

    script_path = scripts_path / f"{script_name}.py"
    if script_path.exists():
        print(f"Script {script_name} already exists")
        return

    script_path.write_text(template.format(script_name=script_name))
    print(f"Created new script: {script_path}")

def list_scripts() -> str:
    """List all available scripts"""
    if len(script_names) == 0:
        return "No scripts found"
    output = "\nAvailable scripts:\n"
    for script_name in script_names:
        module = import_from_path(script_name + ".py", (scripts_path / f"{script_name}.py").absolute())
        doc = module.main.__doc__ if hasattr(module, "main") and module.main.__doc__ else "No documentation"
        output += f"  - {script_name}: {doc}\n"
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(epilog=list_scripts())
    subparsers = parser.add_subparsers(dest='command')

    # Run command
    run_parser = subparsers.add_parser('run', help=run.__doc__)
    run_parser.add_argument('script_name', choices=script_names)
    run_parser.add_argument('args', nargs='*', help='Positional arguments')
    run_parser.add_argument('--kwargs', nargs='*', action='append',
                           help='Keyword arguments as key value pairs')

    # New command
    new_parser = subparsers.add_parser('new', help=new.__doc__)
    new_parser.add_argument('script_name')

    # List command
    subparsers.add_parser('list', help=list_scripts.__doc__)

    args = parser.parse_args()

    command_handlers = {
        'run': lambda: run(args.script_name, args.args or [], {} if not args.kwargs else dict(zip(args.kwargs[0][::2], args.kwargs[0][1::2]))),
        'new': lambda: new(args.script_name),
        'list': lambda: print(list_scripts())
    }

    if len(vars(args)) == 0 or not args.command:
        parser.print_help()
    else:
        command_handlers[args.command]()
