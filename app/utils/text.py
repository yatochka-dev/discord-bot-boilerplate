import re


def convert_text_to_bold(string: str, /) -> str:
    return "\033[1m" + string + "\033[0m"


def get_mentions_as_list(text: str) -> list[str]:
    return re.findall(r"<@!\d+>|<@&\d+>|<#\d+>|<@\d+>|@everyone|@here", text)


def get_mentions_as_string(text: str, /) -> str:
    mentions = get_mentions_as_list(text)
    return " ".join(mentions)
