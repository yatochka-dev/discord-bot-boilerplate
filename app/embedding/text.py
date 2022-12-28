__all__ = ["md", "CodeBlock"]


class DiscordFormattingMethod:
    spec_name_to_scopes = {
        "bold": "**",
        "italic": "*",
        "underline": "__",
        "strikethrough": "~~",
        "code": "`",
        "spoiler": "||",
    }

    def __init__(self, string: str, **kwargs):
        self.string = string

    def __str__(self):
        return self.string

    def __repr__(self):
        return f"{self.__class__.__name__}({self.string!r})"

    def __format__(self, format_spec):
        scopes = self.spec_name_to_scopes.get(format_spec, "")
        return f"{scopes}{self.string}{scopes}"


class CodeBlock(DiscordFormattingMethod):
    def __init__(self, string, language: str = None):
        super().__init__(string)
        self.language = language

    def __str__(self):
        return f"```{self.language}\n{self.string}\n```"


md = DiscordFormattingMethod
