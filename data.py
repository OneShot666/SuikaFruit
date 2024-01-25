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

# Difficulty info (determine size of fruit)
# Easy : smaller fruits, dist to merge lower (x0.9)
# Medium : Default parameters
# Hard : bigger fruits, dist to merge larger (x1.1)
# Impossible : giant fruits, dist to merge larger (x1.25), only first 4 fruit

SkinsDict = {
    "ball": {"cherry": "golf", "strawberry": "billiard", "grape": "base", "clementine": "tennis",
           "orange": "cricket", "apple": "palm", "pear": "bowling", "peach": "beach",
           "pineapple": "volley", "melon": "foot", "watermelon": "basket"},
    "cake": {"cherry": "cherry", "strawberry": "straw", "grape": "graperoll", "clementine": "croissant",
           "orange": "pretzel", "apple": "cookie", "pear": "muffin", "peach": "donut",
           "pineapple": "icecream", "melon": "cupcake", "watermelon": "pancake"},
    "candy": {"cherry": "spiral", "strawberry": "dot", "grape": "caramel", "clementine": "egg",
            "orange": "trine", "apple": "rope", "pear": "bean", "peach": "heart",
            "pineapple": "star", "melon": "menthol", "watermelon": "jelly"},
    "fruit": {"cherry": "cherry", "strawberry": "strawberry", "grape": "grape", "clementine": "clementine",
            "orange": "orange", "apple": "apple", "pear": "pear", "peach": "peach",
            "pineapple": "pineapple", "melon": "melon", "watermelon": "watermelon"},
    "organ": {"cherry": "blood", "strawberry": "tooth", "grape": "kidney", "clementine": "bladder",
            "orange": "spleen", "apple": "heart", "pear": "stomach", "peach": "liver",
            "pineapple": "lung", "melon": "gut", "watermelon": "brain"},
    "planet": {"cherry": "pluto", "strawberry": "moon", "grape": "mercury", "clementine": "mars",
             "orange": "venus", "apple": "earth", "pear": "neptun", "peach": "uranus",
             "pineapple": "saturn", "melon": "jupiter", "watermelon": "sun"},
    "shell": {"cherry": "snail", "strawberry": "ray", "grape": "violet", "clementine": "fan",
            "orange": "golden", "apple": "crimson", "pear": "sunrise", "peach": "twilight",
            "pineapple": "clap", "melon": "pearl", "watermelon": "house"},
    "vegetable": {"cherry": "pea", "strawberry": "garlic", "grape": "radish", "clementine": "corn",
            "orange": "broccoli", "apple": "tomato", "pear": "pepper", "peach": "potato",
            "pineapple": "eggplant", "melon": "salad", "watermelon": "pumpkin"}}
