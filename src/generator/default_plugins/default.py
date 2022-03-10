from generator.pluggability.plugin import Plugin
class DefaultPlugin(Plugin):
    def get_strategies(self, args):
        return []
