from generator.pluggability.plugin import Plugin
from generator.default_plugins.strategies.params import DefaultParams
class DefaultPlugin(Plugin):
    def get_strategies(self, args):
        return [DefaultParams(args)]
