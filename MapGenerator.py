from PIL import Image

from Map import *
from Utils import *
from Colour import *

print("Preparing... \n");


image = Image.new("RGB", (mapSize,mapSize))
targetGenerator = None

targetGenerator = MapGen_Main();

print("Processing map... \n");

targetGenerator.GenerateFull();

print("\n\nGeneration finished. Saving output as GeneratedMap.png.");

for x in range(0, mapSize):
    for y in range(0, mapSize):
        image.putpixel((x,y), colorMap[x][y].GetTuple());

image.save("GeneratedMap.png");
image.show();