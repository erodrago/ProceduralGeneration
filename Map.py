from Colour import *
import random

random.seed(1000)
perlinOffset = random.randint(25,500); # random offset

MapSize = 2048; # size in pixels
g = get_gradient((2,3))
perlinScale = g[0];

mapCenter = (MapSize/2, MapSize/2);

landThreshold = 0.1;

heightMap = [[0]*MapSize for x in range(MapSize)]
colorMap = [[Color() for j in range(MapSize)] for i in range(MapSize)]

randomColorRange = 10;
colorPerlinScale = g[1];
