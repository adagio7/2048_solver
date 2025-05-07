from dataclasses import dataclass
from typing import Callable, List

@dataclass
class Slides:
    start: tuple[int, int]
    end: tuple[int, int]
    value: int
    duration: float
    elapsed: float

@dataclass
class Pops:
    coords: tuple[int, int]
    value: int
    duration: float
    elapsed: float

class Animator:
    def __init__(
        self,
        draw_tile_fn: Callable[[int, tuple[float, float], float], None],
        cell_center_fn: Callable[[int, int], tuple[int, int]],
    ):
        """
        Animator class to handle animations for the game.

        :param draw_tile_fn: Function to draw the tile.
        :param cell_center_fn: Function to get the coords of a cell
        """
        self.draw_tile_fn = draw_tile_fn
        self.cell_center_fn = cell_center_fn
        self.slides: List[Slides] = []
        self.pops: List[Pops] = []

    @property
    def slides_running(self):
        return any(s.elapsed < s.duration for s in self.slides)

    @property
    def pops_running(self):
        return any(p.elapsed < p.duration for p in self.pops)

    @property
    def is_animating(self):
        return self.slides_running or self.pops_running

    def start_slide(
        self,
        grid: list[list[int]],
        moves: dict[tuple[int,int], tuple[int,int]],
        duration: float = 150
    ):
        """
        Start a slide animation for the given grid.
        """
        self.slides.clear()
        for start, end in moves.items():
            value = grid[start[0]][start[1]]

            # Only interested in non-empty cells
            if value:
                self.slides.append(
                    Slides(
                        start=start,
                        end=end,
                        value=value,
                        duration=duration,
                        elapsed=0,
                    )
                )

    def start_pop(
        self,
        grid: list[list[int]],
        merges: set[tuple[int,int]],
        duration: float = 100
    ):
        self.pops.clear()
        for coords in merges:
            value = grid[coords[0]][coords[1]]

            # Only interested in non-empty cells
            if value:
                self.pops.append(
                    Pops(
                        coords=coords,
                        value=value,
                        duration=duration,
                        elapsed=0,
                    )
                )

    def update(self, dt):
        """Advance all animations by dt milliseconds."""
        for s in self.slides:
            s.elapsed = min(s.elapsed + dt, s.duration)

        for p in self.pops:
            p.elapsed = min(p.elapsed + dt, p.duration)

    def draw(self, grid):
        """Draw the animation by iterating over the slides and pops."""

        # Avoid drawing over the slides and pops
        busy = {
          *{s.start for s in self.slides},
          *{s.end   for s in self.slides},
          *{p.coords for p in self.pops},
        }

        # Draw tiles that are unmoved / unaffected
        for j,row in enumerate(grid):
            for i,val in enumerate(row):
                if val and (i,j) not in busy:
                    center = self.cell_center_fn(i,j)
                    self.draw_tile_fn(val, center, 1.0)

        for s in self.slides:
            t = min(s.elapsed / s.duration, 1.0)
            x0,y0 = self.cell_center_fn(*s.start)
            x1,y1 = self.cell_center_fn(*s.end)
            # TODO: currently uses linear interpolation
            # but we could use some smoothing
            pos = (x0 + (x1-x0)*t, y0 + (y1-y0)*t)
            self.draw_tile_fn(s.value, pos, 1.0)

        for p in self.pops:
            t = min(p.elapsed / p.duration, 1.0)
            scale = 1.0 + 0.2*(1 - abs(2*t - 1))  
            center = self.cell_center_fn(*p.coords)
            self.draw_tile_fn(p.value, center, scale)
