import math


def collision_point_cercle(point, centre_cercle, rayon_cercle):
    # Point : (x, y)
    # Centre du cercle : (x, y)
    # Rayon du cercle : float

    distance = math.sqrt((point[0] - centre_cercle[0])**2 + (point[1] - centre_cercle[1])**2)

    return distance <= rayon_cercle


# Exemple d'utilisation
centre_cercle = (0, 0)
rayon_cercle = 5

point_test = (3, 4)

if collision_point_cercle(point_test, centre_cercle, rayon_cercle):
    print("Le point est à l'intérieur ou sur le cercle.")
else:
    print("Le point est à l'extérieur du cercle.")
