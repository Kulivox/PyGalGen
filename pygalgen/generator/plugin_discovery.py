"""
Module responsible for plugin discovery, configuration and initialization
"""
import importlib
import importlib.util
import pkgutil
import inspect
import sys
from importlib.abc import Traversable

from pygalgen.generator.pluggability.plugin import Plugin
from typing import Any, Union, List
import os
import yaml
import logging


class PluginDiscoveryException(Exception):
    pass


def get_plugin_configuration(config_file_path: str) -> dict[str, Any]:
    """

    Parameters
    ----------
    config_file_path : str

    Returns
    -------
    Dictionary containing parsed yml file

    """
    with open(config_file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_plugin(configuration: dict[str, Any], plugin_dir: str) -> Plugin:
    """
    The function initializes plugin based on provided configuration and path

    Parameters
    ----------
    configuration : dict[str, Any]
     parsed configuration yaml
    plugin_dir : str
     path to the root directory of plugin

    Returns
    -------
    plugin : Plugin
     initialized plugin object
    """
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

    path_to_module, module_name = os.path.split(plugin_dct["path"])
    module_name = os.path.splitext(module_name)[0]
    file_path = os.path.join(plugin_dir, plugin_dct["path"])

    # Beware, what follows is a revoltingly dirty hack to solve import problems
    plugin_module_dir_path = os.path.join(plugin_dir, path_to_module)
    sys.path.append(plugin_module_dir_path)

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

    assets_path = None
    if "assets" in plugin_dct and plugin_dct["assets"] is not None:
        assets_path = os.path.join(plugin_dir, plugin_dct["assets"])

    return classes[0](plugin_dct.get("order", 0), plugin_dct["name"],
                      assets_path)


def discover_plugins(path: Union[str, Traversable]) -> List[Plugin]:
    """
    Function traverses directory structure with path as a root and loads
    all discovered plugins
    The plugins have to have valid configuration file to be

    Parameters
    ----------
    path : Union[str, Traversable]
     path to the root directory of plugins

    Returns
    -------
    result : List[Plugin]
     list of initialized plugins

    Raises
    -------
    FileNotFoundError
     raises FileNotFoundError in case plugin configuration points
     to missing plugin module

    """
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
