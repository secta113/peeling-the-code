from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Campaign:
    end: date

    def applies(self) -> bool:
        return date.today() <= self.end
