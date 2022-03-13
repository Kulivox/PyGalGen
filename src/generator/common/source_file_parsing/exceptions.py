class ArgumentParsingDiscoveryError(Exception):
    pass

class ArgParseImportNotFound(ArgumentParsingDiscoveryError):
    pass


class ArgParserNotUsed(ArgumentParsingDiscoveryError):
    pass