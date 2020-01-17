class BaseMapGenerator:
    
    def __init__(self):    # Constructor
        self.progress = 0
        self.totalProgress = MapSize * MapSize
        self.isFinished = False
        self.pbar = tqdm(total = MapSize * MapSize)
        self.pbar.clear()
        self.smartGenerationEnabled = False
        self.x = 0
        self.y = 0

    def GenPixel(self, x, y): # Generates a pixel
        self.x += 1
        if (self.x >= MapSize):
            self.x = 0
            self.y += 1
            if (self.y >= MapSize):
                self.isFinished = True
                self.pbar.close()
        print(x + " " + y)
        
    def GenFull(self): # fully generate
        g = get_gradient((2,3))
        gradient = g[1]
        for x in range(0, MapSize):
            for y in range(0, MapSize):
                self.Generate(x,y,gradient)

class MainMapGenerator(BaseMapGenerator): # gets base perlin height, make terrain and water
    
    def Generate(self, x, y, gradient): 
        
        if (self.smartGenerationEnabled):
            self.x += 1
            if (self.x >= MapSize):
                self.x = 0
                self.y += 1
                if (self.y >= MapSize):
                    self.isFinished = True
                    self.pbar.close()
        #perlin noise
        PerlinBaseValue = (snoise2(float(x)*perlinScale, float(y)*perlinScale, octaves=8, persistence=0.5, lacunarity=2.0, repeatx=2048, repeaty=2048, base=perlinOffset) + 1)/2.0

        # pixel height
        distance = DistanceNormalized(x,y, mapCenter[0], mapCenter[1], MapSize)

        PerlinBaseValue -= math.pow(distance, 0.5)
        if (PerlinBaseValue <= 0):
            PerlinBaseValue = 0

        heightMap[x][y] = PerlinBaseValue

        # pixel color
        if (heightMap[x][y] > landThreshold): #land

            detailPerlinValue = (snoise2(float(x)*perlinScale, float(y)*perlinScale, octaves=12, persistence=0.8, lacunarity=2.0, repeatx=2048, repeaty=2048, base=perlinOffset) + 1)/2.0

            normalizedHeight = (detailPerlinValue - landThreshold)
            normalizedHeight *= normalizedHeight*normalizedHeight; # normalized height ^3

            noiseValue = (snoise2(float(x)*colorPerlinScale, float(y)*colorPerlinScale, octaves=2, persistence=0.5, lacunarity=2.0, repeatx=2048, repeaty=2048, base=perlinOffset) + 1)/2.0
            randomColorOffset = (random.random()-0.5)*8 + 24.0*noiseValue + normalizedHeight*256.0

            r = groundColor.r + randomColorOffset
            g = groundColor.g + randomColorOffset
            b = groundColor.b + randomColorOffset
            
            # Add color to pixel
            colorMap[x][y].SetColor(r,g,b)

        else: #water

            normalizedHeight = (heightMap[x][y])
            

            if (normalizedHeight < 0):
                normalizedHeight = 0
            
            waterNoisePerlinScale = gradient

            noiseValue = (snoise2(float(x)*waterNoisePerlinScale, float(y)*waterNoisePerlinScale, octaves=2, persistence=0.5, lacunarity=2.0, repeatx=2048, repeaty=2048, base=perlinOffset) + 1)/2.0;
            randomColorOffset = (random.random()-0.5)*4 + 12.0*noiseValue + normalizedHeight*96.0;

            r = waterColor.r + randomColorOffset
            g = waterColor.g + randomColorOffset
            b = waterColor.b + randomColorOffset

            if (r < 0):
                r = 0
            if (g < 0):
                g = 0
            if (b < 0):
                b = 0

            colorMap[x][y].SetColor(r,g,b)

        self.pbar.update(1); #updates the progress bar



def Distance(ax = 0.0, ay = 0.0, cx = 0.0, cy = 0.0):
    x = ax - cx
    x *= x
    y = ay - cy
    y *= y
    return (math.sqrt(x + y))

def DistanceNormalized(ax = 0.0, ay = 0.0, cx = 0.0, cy = 0.0, size = 256):
    dist = Distance(ax, ay, cx, cy)
    dist /= size
    return dist