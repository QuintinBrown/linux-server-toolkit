import importlib
from pathlib import Path

PLUGIN_PACKAGE = "plugins"
PLUGIN_DIR = Path(__file__).resolve().parent.parent / "plugins"

def load_plugins():
    plugins = []

    for plugin_file in PLUGIN_DIR.glob("*.py"):
        if plugin_file.name.startswith("__"): # skips special files
            continue

        module_name = plugin_file.stem # get filename without .py extension
        module_path = f"{PLUGIN_PACKAGE}.{module_name}" # plugins.example_plugin

        try:
            module = importlib.import_module(module_path)
            # instantiate Plugin class from module
            plugin = module.Plugin()
            plugins.append(plugin)

        except Exception as e:
            print(f"[FAILED LOADING PLUGIN] {module_name} {e}")

    return plugins