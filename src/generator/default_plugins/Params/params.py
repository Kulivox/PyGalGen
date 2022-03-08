from generator.pluggability.plugin import Plugin
from .params_strategy import ParamsStrategy

class Params(Plugin):
    def get_strategies(self):
        return [ParamsStrategy()]
