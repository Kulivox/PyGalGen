from generator.pluggability.plugin import Plugin
from generator.plugins.custom_strategy import CustomStrategy

class CustomPlugin(Plugin):
    def get_strategies(self, args):
        return [CustomStrategy(args)]
