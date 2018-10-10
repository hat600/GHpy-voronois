# GHpy-voronois

generates voronoi diagram under Manhattan distance (taxicab geometry), or Chebyshev distance.

it works in GHpython, under Grasshopper3d, Rhinoceros 6.

make a GHpython battery with 2 inputs:
* P: source points (Point3d, List Access)
* r: radius (float, Item Access）

and 1 output:
* PL

it gerenates closed Polyline for each cell.

at this point, border is not cut.

for future updates, there might be border-cutting, and change of planes.
