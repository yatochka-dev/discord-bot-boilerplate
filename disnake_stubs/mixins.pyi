from typing import overload


class Hashable:

    @overload
    @property
    def snowflake(self) -> str: ...
