def parse_argument_comma_sep_list(argument: str):
    for item in argument.split(","):
        yield tuple(item.split(":"))