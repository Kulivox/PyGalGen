import importlib
import importlib.util
import pkgutil
import inspect
from importlib.abc import Traversable

from pygalgen.generator.pluggability.plugin import Plugin
from typing import Any, Union
import os
import yaml
import logging


class PluginDiscoveryException(Exception):
    pass


def get_plugin_configuration(config_file_path) -> dict[str, Any]:
    with open(config_file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_plugin(configuration: dict[str, Any], plugin_dir: str) -> Plugin:
    plugin_dct = configuration["plugin"]

    installed_modules = set(name for _, name, _ in pkgutil.iter_modules())
    # check whether required modules of this plugin are available
    for req in plugin_dct["requirements"]:
        if req not in installed_modules:
            logging.warning(f"Loading of plugin '{plugin_dct['name']}' "
                            f"failed. Reason: requirement '{req}' of this "
                            f"plugin "
                            f"can't be satisfied")
            raise PluginDiscoveryException()

    _, module_name = os.path.split(plugin_dct["path"])
    module_name = os.path.splitext(module_name)[0]
    file_path = os.path.join(plugin_dir, plugin_dct["path"])

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    classes = [class_ for _, class_ in inspect.getmembers(module,
                                                          lambda member:
                                                          inspect.isclass(
                                                              member) and
                                                          member != Plugin and
                                                          issubclass(member,
                                                                     Plugin))]

    if not classes:
        logging.warning(f"No plugins were declared in"
                        f" {plugin_dct['path']}")
        raise PluginDiscoveryException()

    if len(classes) > 1:
        logging.warning(f"More than one plugin definition detected in"
                        f" {plugin_dct['path']}")
        raise PluginDiscoveryException()

    return classes[0](os.path.join(plugin_dir, plugin_dct["assets"]))


def discover_plugins(path: Union[str, Traversable]):
    try:
        result = []
        for path, _, files in os.walk(path):
            for file in files:
                if file.endswith(".yml"):
                    try:
                        file_path = os.path.join(path, file)
                        conf = get_plugin_configuration(file_path)
                        result.append(load_plugin(conf, path))
                    except PluginDiscoveryException:
                        continue

        return result

    except FileNotFoundError:
        raise PluginDiscoveryException("Plugin discovery failed")
