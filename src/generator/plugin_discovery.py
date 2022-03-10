import importlib
import pkgutil
import inspect
from generator.pluggability.plugin import Plugin
from typing import List

def discover_plugins(namespace):
    namespace_iterator = pkgutil.iter_modules(namespace.__path__,
                                              namespace.__name__ + ".")
    modules =\
        [importlib.import_module(name) for _, name, _ in namespace_iterator]

    plugins: List[Plugin] = []
    for module in modules:
        classes = inspect.getmembers(module,
                                     lambda member:
                                     inspect.isclass(member) and
                                     member != Plugin and
                                     issubclass(member, Plugin))

        plugins += [cls() for _, cls in classes]

    return plugins
