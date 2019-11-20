from dataclasses import dataclass, fields
from pathlib import Path


@dataclass
class Replies:
    start: str = ""
    help: str = ""

    @classmethod
    def load_from_dir(cls, path: Path):
        instance = cls()
        dc_fields = {f.name for f in fields(instance)}
        for p in path.iterdir():
            if p.is_file() and p.stem in dc_fields:
                with p.open() as f:
                    setattr(instance, p.stem, f.read())

        return instance
