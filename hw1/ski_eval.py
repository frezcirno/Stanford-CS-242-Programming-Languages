import src.ski as ski


##########
# PART 1 #
##########
# TASK: Implement the below function `eval`.


class Kx(ski.Expr):
    def __init__(self, x):
        self.x = x


class Sx(ski.Expr):
    def __init__(self, x):
        self.x = x


class Sxy(ski.Expr):
    def __init__(self, x, y):
        self.x = x
        self.y = y


def eval(e: ski.Expr) -> ski.Expr:
    # BEGIN_YOUR_CODE
    if isinstance(e, ski.App):
        e1 = eval(e.e1)
        # I x => x
        if isinstance(e1, ski.I):
            return eval(e.e2)
        # K x => Kx
        elif isinstance(e1, ski.K):
            return Kx(eval(e.e2))
        # Kx y => x
        elif isinstance(e1, Kx):
            return e1.x  # e1.x is already evaluated
        # S x => Sx
        elif isinstance(e1, ski.S):
            return Sx(eval(e.e2))
        # Sx y => Sxy
        elif isinstance(e1, Sx):
            return Sxy(e1.x, eval(e.e2))
        # Sxy z = x z (y z)
        elif isinstance(e1, Sxy):
            z = eval(e.e2)
            xz = eval(ski.App(e1.x, z))
            yz = eval(ski.App(e1.y, z))
            return eval(ski.App(xz, yz))
    return e

    # END_YOUR_CODE
