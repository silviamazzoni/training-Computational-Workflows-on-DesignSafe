# Silvia Mazzoni, 2025
import os
import pkgutil
import importlib

def import_all_flat(package_name):
    base_path = os.path.dirname(__file__)
    for _, module_name, ispkg in pkgutil.walk_packages([base_path], prefix=f"{package_name}."):
        if ispkg or module_name.endswith("opsUtils"):
            continue
        module = importlib.import_module(module_name)
        for attr in dir(module):
            if not attr.startswith("_"):  # skip private/dunder names
                item = getattr(module, attr)
                if callable(item):
                    globals()[attr] = item

# Use it for your current package
import_all_flat("OpsUtils")
