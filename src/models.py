from enum import Enum
from typing import TypeAlias, List, Tuple

Cell: TypeAlias = int
Row: TypeAlias = List[Cell]
Grid: TypeAlias = List[Row]

Coords: TypeAlias = Tuple[int, int]
AnimationSlides: TypeAlias = dict[Coords, Coords]
AnimationMerges: TypeAlias = dict[Coords, int]

class Moves(Enum):
    LEFT   = 'left'
    RIGHT  = 'right'
    UP     = 'up'
    DOWN   = 'down'
