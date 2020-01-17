from Colour import *
import random
from qiskit import QuantumCircuit, execute, Aer
from math import pi
import numpy as np

def get_gradient( pos, seed=10 ):
    ''' Uses quantum circuit to create Random values for gradient '''
    
    (x,y) = pos
    
    # initialize a circuit
    # arbitrarily chosen to have 2 qubits
    qc = QuantumCircuit(2,2)

    # fill the circuits with gates that depend on x,y and seed
    # (arbitrarily chosen)
    for j in range(seed):
        qc.ry(x*pi/seed,0)
        qc.ry(y*pi/seed,1)
        qc.cx(0,1)
        
    # put in some measure gates so we can get an output
    qc.measure(0,0)
    qc.measure(1,1)
    
    # run and get the counts dict
    counts = execute(qc,Aer.get_backend('qasm_simulator')).result().get_counts()

    # make sure that every possible output has a non-zero entry in the counts dict
    for output in ['00', '10', '11', '01']:
        if output not in counts:
            counts[output] = 1
            
    # use a couple of these numbers to define the 2D vector
    # (arbitrarily chosen to be the counts for 11 and 01
    print(counts)
    gradient = [counts['00'],counts['11'],counts['10'], counts['01']]
    # normalize the vector
    length = np.sqrt( gradient[0]**2 + gradient[1]**2 + gradient[2]**2 + gradient[3]**2)
    gradient = [ gradient[1]/length, gradient[3]/length ]
    
    # and output it
    return gradient

random.seed(1000)
perlinOffset = random.randint(25,500); # random offset

MapSize = 2048; # size in pixels
g = get_gradient((2,3))
perlinScale = g[0]

mapCenter = (MapSize/2, MapSize/2)

landThreshold = 0.1

heightMap = [[0]*MapSize for x in range(MapSize)]
colorMap = [[Color() for j in range(MapSize)] for i in range(MapSize)]

randomColorRange = 10
colorPerlinScale = g[1]
