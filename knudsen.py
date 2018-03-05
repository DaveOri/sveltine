import numpy as np
from sys import argv

scriptname, Temperature, pressure, diameter, Length = argv

Temperature = float(Temperature)
pressure = float(pressure)
diameter = float(diameter)
Length = float(Length)

boltzmann_constant = 1.380650424e-23

lambd = boltzmann_constant*Temperature/(np.sqrt(2)*np.pi*diameter**2.0*pressure)
Kn = lambd/Length

print('Mean free path ',lambd)
print('Knudsen number ',Kn)
