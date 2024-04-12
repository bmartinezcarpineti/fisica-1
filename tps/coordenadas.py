import math

def cartesianas_a_polares(x, y):

    r = math.sqrt(x**2 + y**2)
    theta = math.atan2(y, x)

    return r, theta

def polares_a_cartesianas(r, theta):

    x = r * math.cos(math.radians(theta))
    y = r * math.sin(math.radians(theta))
    
    return x, y