# TODO: refactor & clean up this class.
#  - Familiarize yourself with the code and what it does (it is easiest to read the tests first)
#  - refactor ...
#     - give the functions/variables proper names
#     - make the function bodies more readable
#     - clean up the test code where beneficial
#     - make sure to put each individual change in a small, separate commit
#     - take care that on each commit, all tests pass
from typing import Tuple
from dataclasses import dataclass


@dataclass
class Point:
    _x: float
    _y: float


class RasterGrid:
    @dataclass
    class Cell:
        _ix: int
        _iy: int

    def __init__(
        self, Point_LowerLeft: Point, Point_UpperRight: Point, nx: int, ny: int
    ) -> None:
        self.Pt_LowerLeft = Point_LowerLeft
        self.Pt_UpperRight = Point_UpperRight
        self._nx = nx
        self._ny = ny
        self.nc = nx * ny
        self.cells = [self.Cell(i, j) for i in range(nx) for j in range(ny)]

    def get_cell_center(self, cell: Cell) -> Point:
        return (
            self.Pt_LowerLeft._x
            + (float(cell._ix) + 0.5)
            * (self.Pt_UpperRight._x - self.Pt_LowerLeft._x)
            / self._nx,
            self.Pt_LowerLeft._y
            + (float(cell._iy) + 0.5)
            * (self.Pt_UpperRight._y - self.Pt_LowerLeft._y)
            / self._ny,
        )

    def calc_eps(self, Pt_LowerLeft: Point, Pt_UpperRight: Point) -> float:
        return 1e-6 * max(
            (Pt_UpperRight._x - Pt_LowerLeft._x) / self._nx,
            (Pt_UpperRight._y - Pt_LowerLeft._y) / self._ny,
        )

    def calc_abs(self, no1: float, no2: float) -> float:
        return abs(no1 - no2)

    def locate_cell(self, Pt: Point) -> Cell:
        eps = self.calc_eps(self.Pt_LowerLeft, self.Pt_UpperRight)

        if self.calc_abs(Pt._x, self.Pt_UpperRight._x) < eps:
            ix = self._nx - 1
        elif self.calc_abs(Pt._x, self.Pt_LowerLeft._x) < eps:
            ix = 0
        else:
            ix = int(
                (Pt._x - self.Pt_LowerLeft._x)
                / ((self.Pt_UpperRight._x - self.Pt_LowerLeft._x) / self._nx)
            )
        if self.calc_abs(Pt._y, self.Pt_UpperRight._y) < eps:
            iy = self._ny - 1
        elif self.calc_abs(Pt._y, self.Pt_LowerLeft._y) < eps:
            iy = 0
        else:
            iy = int(
                (Pt._y - self.Pt_LowerLeft._y)
                / ((self.Pt_UpperRight._y - self.Pt_LowerLeft._y) / self._ny)
            )
        return self.Cell(ix, iy)


def test_number_of_cells():
    x0 = 0.0
    y0 = 0.0
    dx = 1.0
    dy = 1.0
    assert RasterGrid(Point(x0, y0), Point(dx, dy), 10, 10).nc == 100
    assert RasterGrid(Point(x0, y0), Point(dx, dy), 10, 20).nc == 200
    assert RasterGrid(Point(x0, y0), Point(dx, dy), 20, 10).nc == 200
    assert RasterGrid(Point(x0, y0), Point(dx, dy), 20, 20).nc == 400


def test_locate_cell():
    grid = RasterGrid(Point(0.0, 0.0), Point(2.0, 2.0), 2, 2)
    cell = grid.locate_cell(Point(0, 0))
    assert cell._ix == 0 and cell._iy == 0
    cell = grid.locate_cell(Point(1, 1))
    assert cell._ix == 1 and cell._iy == 1
    cell = grid.locate_cell(Point(0.5, 0.5))
    assert cell._ix == 0 and cell._iy == 0
    cell = grid.locate_cell(Point(1.5, 0.5))
    assert cell._ix == 1 and cell._iy == 0
    cell = grid.locate_cell(Point(0.5, 1.5))
    assert cell._ix == 0 and cell._iy == 1
    cell = grid.locate_cell(Point(1.5, 1.5))
    assert cell._ix == 1 and cell._iy == 1


def test_cell_center():
    grid = RasterGrid(Point(0.0, 0.0), Point(2.0, 2.0), 2, 2)
    cell = grid.locate_cell(Point(0.5, 0.5))
    assert (
        abs(grid.get_cell_center(cell)[0] - 0.5) < 1e-7
        and abs(grid.get_cell_center(cell)[1] - 0.5) < 1e-7
    )
    cell = grid.locate_cell(Point(1.5, 0.5))
    assert (
        abs(grid.get_cell_center(cell)[0] - 1.5) < 1e-7
        and abs(grid.get_cell_center(cell)[1] - 0.5) < 1e-7
    )
    cell = grid.locate_cell(Point(0.5, 1.5))
    assert (
        abs(grid.get_cell_center(cell)[0] - 0.5) < 1e-7
        and abs(grid.get_cell_center(cell)[1] - 1.5) < 1e-7
    )
    cell = grid.locate_cell(Point(1.5, 1.5))
    assert (
        abs(grid.get_cell_center(cell)[0] - 1.5) < 1e-7
        and abs(grid.get_cell_center(cell)[1] - 1.5) < 1e-7
    )


def test_cell_iterator() -> None:
    grid = RasterGrid(Point(0.0, 0.0), Point(2.0, 2.0), 2, 2)
    count = sum(1 for _ in grid.cells)
    assert count == grid.nc

    cell_indices_without_duplicates = set(
        list((cell._ix, cell._iy) for cell in grid.cells)
    )
    assert len(cell_indices_without_duplicates) == count
