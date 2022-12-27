def bold(_: str, /) -> str:
    return "\033[1m" + _ + "\033[0m"
