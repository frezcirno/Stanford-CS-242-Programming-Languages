import src.lam as lam
import src.ski as ski

##########
# PART 3 #
##########
# TASK: Implement the below function `tran`.
# You can define helper functions outside `tran` and use them inside `tran`.


def tranu(s: str, e: ski.Expr) -> ski.Expr:
    # U(x, I) = K I
    # U(x, S) = K S
    # U(x, K) = K K
    if isinstance(e, (ski.I, ski.S, ski.K)):
        return ski.App(ski.K(), e)
    # U(x, x) = I
    elif isinstance(e, ski.Var) and e.s == s:
        return ski.I()
    # U(x, y) = K y
    elif isinstance(e, ski.Var):
        return ski.App(ski.K(), e)
    # U(x, (e1 e2)) = S (U(x, e1)) (U(x, e2))
    elif isinstance(e, ski.App):
        return ski.App(ski.App(ski.S(), tranu(s, e.e1)), tranu(s, e.e2))
    raise RuntimeError


def tran(e: lam.Expr) -> ski.Expr:
    # BEGIN_YOUR_CODE
    if isinstance(e, lam.Var):
        return ski.Var(e.s)
    elif isinstance(e, lam.Lam):
        return tranu(e.s, tran(e.e))
    elif isinstance(e, lam.App):
        return ski.App(tran(e.e1), tran(e.e2))
    raise RuntimeError
    # END_YOUR_CODE
