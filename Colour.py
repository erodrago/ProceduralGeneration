class Color:

    r = 0.0;
    g = 0.0;
    b = 0.0;
    a = 1.0;

    def __init__(self, r = 0.0, g = 0.0, b = 0.0):
        self.r = r;
        self.g = g;
        self.b = b;
        self.a = 1;
    def GetTuple(self):
        return (int(self.r),int(self.g),int(self.b));
    def SetColor(self, r, g, b):
        self.r = r;
        self.g = g;
        self.b = b;

        
paperColor = Color(212, 161, 104);
waterColor = Color(48, 86, 181);