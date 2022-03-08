from generator.pluggability.plugin import Plugin
from .custom_strategy import CustomStrategy

class CustomPlugin(Plugin):
    def get_strategies(self):
        return [CustomStrategy()]