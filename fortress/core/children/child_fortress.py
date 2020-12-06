from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fortress import Fortress


class ChildFortress:
    def __init__(self):
        super().__init__()
        self._fortress = None

    def set_fortress(self, fortress: "Fortress"):
        self._fortress = fortress

    @property
    def fortress(self) -> "Fortress":
        return self._fortress
