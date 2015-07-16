def to_coords(pos):
    return (pos['x'], pos['y'])

def addvec(pos, unit_vector):
    xoff, yoff = unit_vector
    return {'x': pos['x'] + xoff,
            'y': pos['y'] + yoff}

def to_pos(coords):
    x, y = coords
    return {'x': x,
            'y': y}
