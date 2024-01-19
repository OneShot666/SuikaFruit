# from math import *
# from random import *
# from time import *

# Real gravitational field intensity
gravity = 9.81                                                                  # Newton / kg
# Real air resistance (! unused since new physics)
resistance = 1.2                                                                # Kg / m^3
# Real max drag coefficient (smooth sphere) (! unused since new physics)
drag_coeff = 0.47                                                               # no unit

# Variables for adjustments (! unused since new physics)
bounce = 0.5                                                                    # Bounce coeff against walls
lift = 1.2                                                                      # Lift coeff for fruit

# Variables of physics
walls_elasticity = 0.2
walls_friction = 0.8
fruit_elasticity = 0.2
fruit_friction = 0.5

# Difficulty info (determine size of fruits)
# Easy : dist to merge lower (x0.9)
# Medium : Default parameters
# Hard : bigger repulsion force (x1.1)
# Impossible : bigger repulsion force (x1.25), only first 4 fruits
