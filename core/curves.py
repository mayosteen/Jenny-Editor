def i_circ(o):
    return 1-(1-o**2)**0.5

def o_circ(o):
    return 1-(o-1)**2


def io_circ(o):
    if o <= 0.5:
        return i_circ(o*2)/2
    else:
        return (o_circ(o*2-1)+1)/2

def io_circle(p0, p1, o):
    o = io_circ(o)
    return (
        p0[0]*(1-o) + p1[0]*o,
        p0[1]*(1-o) + p1[1]*o,
    )