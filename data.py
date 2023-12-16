# from math import *
# from random import *
# from time import *

# Real gravitational field intensity
gravity = 9.8                                                                   # Newton / kg
# Real air resistance
resistance = 1.2                                                                # Kg / m^3
# Real max drag coefficient (smooth sphere)
drag_coeff = 0.47                                                               # no unit

# Variables for adjustments
bounce = 0.25                                                                   # Bounce coeff against walls
lift = 1.5                                                                      # Lift coeff for fruit

# Difficulty info
# Easy : dist to merge lower (x0.9)
# Medium : Default parameters
# Hard : bigger repulsion force (x1.1)
# Impossible : bigger repulsion force (x1.25), only first 4 fruits
