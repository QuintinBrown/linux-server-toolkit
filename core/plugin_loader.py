import importlib
from pathlib import Path

PLUGIN_PACKAGE = "plugins"
PLUGIN_DIR = Path(__file__).resolve().parent.parent / "plugins"

def load_plugins():
    plugins = []

    for plugin_file in PLUGIN_DIR.glob("*.py"):
        if plugin_file.name.startswith("__"):
            continue

        module_name = plugin_file.stem
        module_path = f"{PLUGIN_PACKAGE}.{module_name}"

        try:
            module = importlib.import_module(module_path)
            plugin = module.Plugin()
            plugins.append(plugin)

        except Exception as e:
            print(f"[FAILED LOADING PLUGIN] {module_name} {e}")

    return plugins