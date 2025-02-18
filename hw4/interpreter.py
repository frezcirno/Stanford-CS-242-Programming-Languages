import src.objc as objc
from typing import Optional, Set


# free_vars is a helper function for the implementation of
# subst that collects all free variables present in an expression.
def free_vars(e: objc.Expr | objc.Method) -> Set[objc.Var]:
    # IMPLEMENT THIS METHOD.
    if isinstance(e, objc.Method):
        return free_vars(e.body) - {e.var}
    elif isinstance(e, objc.Var):
        return {e}
    elif isinstance(e, objc.FieldAccess):
        return free_vars(e.expr)
    elif isinstance(e, objc.MethodOverride):
        return free_vars(e.expr) | free_vars(e.method)
    elif isinstance(e, objc.Object):
        return {v for m in e.fields.values() for v in free_vars(m)}
    else:
        raise ValueError(f"Invalid body: {e}")


# subset_method substitutes expressions for variables within
# a method.
def subst_method(f: objc.Method, x: objc.Var, e: objc.Expr) -> objc.Method:
    # IMPLEMENT THIS METHOD.
    if f.var in free_vars(f) or f.var in free_vars(e) or f.var == x:
        # Rename the variable to avoid capture.
        new_var = objc.Var(f.var.name + "'")
        new_f = objc.Method(new_var, subst(f.body, f.var, new_var))
        return subst_method(new_f, x, e)
    return objc.Method(f.var, subst(f.body, x, e))


# subst implements substitution of variables into expressions. In particular,
# subst(e1, x, e2) substitutes e2 for x in e1, written as e1{x := e2}.
def subst(e1: objc.Expr, x: objc.Var, e2: objc.Expr) -> objc.Expr:
    # IMPLEMENT THIS METHOD.
    if isinstance(e1, objc.Var):
        if e1 == x:
            return e2
        return e1
    elif isinstance(e1, objc.FieldAccess):
        return objc.FieldAccess(subst(e1.expr, x, e2), e1.field)
    elif isinstance(e1, objc.MethodOverride):
        return objc.MethodOverride(
            subst(e1.expr, x, e2),
            e1.field,
            subst_method(e1.method, x, e2),
        )
    elif isinstance(e1, objc.Object):
        return objc.Object(
            [(field, subst_method(m, x, e2)) for field, m in e1.fields.items()]
        )
    else:
        raise ValueError(f"Invalid body: {e1}")


# try_step implements the small-step operational semantics for the
# object calculus. try_step takes an expression e and returns None
# if the expression cannot take a step, or e', where e -> e' in one
# step.
def try_step(e: objc.Expr) -> Optional[objc.Expr]:
    # IMPLEMENT THIS METHOD.
    if isinstance(e, objc.FieldAccess):
        inner = try_step(e.expr)  # Field-Access-Step
        if inner is not None:
            return objc.FieldAccess(inner, e.field)

        if isinstance(e.expr, objc.Object):
            for field, m in e.expr.fields.items():  # Field-Access-Eval
                if field == e.field:
                    return subst(m.body, m.var, e.expr)

        return None

    elif isinstance(e, objc.MethodOverride):
        inner = try_step(e.expr)  # Override-Step
        if inner is not None:
            return objc.MethodOverride(inner, e.field, e.method)

        if isinstance(e.expr, objc.Object):  # Override-Eval
            new_obj = [(f, m) for f, m in e.expr.fields.items() if f != e.field]
            new_obj.append((e.field, e.method))
            return objc.Object(new_obj)

        return None
