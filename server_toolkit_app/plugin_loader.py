import importlib
from pathlib import Path

PLUGIN_PACKAGE = "plugins"
PLUGIN_DIR = Path(__file__).resolve().parent.parent / "plugins"

def load_plugins(output_func=None):
    plugins = []

    for plugin_file in PLUGIN_DIR.glob("*.py"):
        if plugin_file.name.startswith("__"): # skips special files
            continue

        module_name = plugin_file.stem # get filename without .py extension
        module_path = f"{PLUGIN_PACKAGE}.{module_name}" # plugins.example_plugin

        try:
            module = importlib.import_module(module_path)
            # instantiate Plugin class from module
            plugin = module.Plugin(output_func=output_func)
            plugins.append(plugin)

        except Exception as e:
            if output_func:
                output_func(f"[FAILED LOADING PLUGIN] {module_name} {e}")
            print(f"[FAILED LOADING PLUGIN] {module_name} {e}")

    return plugins