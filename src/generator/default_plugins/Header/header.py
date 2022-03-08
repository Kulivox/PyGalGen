from generator.pluggability.plugin import Plugin
from generator.default_plugins.Header.header_strategy import HeaderStrategy

class Header(Plugin):
    def get_strategies(self):
        return [HeaderStrategy()]
