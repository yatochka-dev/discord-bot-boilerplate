def convert_text_to_bold(string: str, /) -> str:
    return "\033[1m" + string + "\033[0m"
