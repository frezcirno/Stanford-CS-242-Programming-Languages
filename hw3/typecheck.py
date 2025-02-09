from src.lam import (
    CONSTS,
    Prog,
    Expr,
    TpVar,
    Var,
    App,
    Lam,
    IntConst,
    Type,
    IntTp,
    Func,
    TypecheckingError,
)
from typing import List
from collections import ChainMap


class Context:
    def __init__(self, ctx=ChainMap(), counter=[0]):
        self._map = ctx
        self._counter = counter

    def push(self):
        return Context(self._map.new_child(), self._counter)

    def pop(self):
        return Context(self._map.parents, self._counter)

    def _newType(self):
        self._counter[0] += 1
        return TpVar("t" + str(self._counter[0]))

    def _resolve(self, tvar, treal):
        for var in self._map:
            self._map[var] = self.__resolve(tvar, treal, self._map[var])
        return treal

    def __resolve(self, tvar, treal, typ):
        if isinstance(typ, TpVar):
            if typ == tvar:
                return treal
        elif isinstance(typ, Func):
            return Func(
                self.__resolve(tvar, treal, typ.a),
                self.__resolve(tvar, treal, typ.b),
            )
        return typ


def resolve(t: Type, t1: Type, t2: Type) -> Type:
    if isinstance(t, TpVar):
        if t == t1:
            return t2
        return t
    elif isinstance(t, Func):
        return Func(resolve(t.a, t1, t2), resolve(t.b, t1, t2))
    return t


def contains(t1: Type, t2: Type) -> bool:
    """Check if t1 contains t2"""
    if t1 == t2:
        return True
    if isinstance(t1, Func):
        return contains(t1.a, t2) or contains(t1.b, t2)


# Match parameter type with argument type, raise if cannot match
def typecheck_app(pTyp: Type, aTyp: Type, _ctx: Context):
    if isinstance(pTyp, IntTp):
        if isinstance(aTyp, IntTp):  # Int, Int
            return
        elif isinstance(aTyp, TpVar):  # Int, TpVar
            _ctx._resolve(aTyp, pTyp)
        elif isinstance(aTyp, Func):  # Int, Func
            raise TypecheckingError(f"Expected {pTyp}, got {aTyp}")
    elif isinstance(pTyp, TpVar):
        if isinstance(aTyp, IntTp):  # TpVar, Int
            _ctx._resolve(pTyp, aTyp)
        elif isinstance(aTyp, TpVar):  # TpVar, TpVar
            _ctx._resolve(aTyp, pTyp)
        else:  # TpVar, Func
            if contains(aTyp, pTyp):
                raise TypecheckingError(f"Recursive type: {pTyp} in {aTyp}")
            _ctx._resolve(pTyp, aTyp)
    else:  # Func
        if isinstance(aTyp, (IntTp,)):  # Func, Int
            raise TypecheckingError(f"Expected {pTyp}, got {aTyp}")
        elif isinstance(aTyp, TpVar):  # Func, TpVar
            _ctx._resolve(aTyp, pTyp)
        else:  # Func, Func
            typecheck_app(pTyp.a, aTyp.a, _ctx)
            typecheck_app(pTyp.b, aTyp.b, _ctx)


def typecheck_expr(expr: Expr, _ctx: Context) -> Type:
    if isinstance(expr, IntConst):
        return IntTp()
    elif isinstance(expr, Var):
        if expr.s in CONSTS:
            return CONSTS[expr.s]
        if expr.s not in _ctx._map:
            raise TypecheckingError(f"Unknown variable {expr.s}")
        return _ctx._map[expr.s]
    elif isinstance(expr, App):  # expr.e1 expr.e2
        t1 = typecheck_expr(expr.e1, _ctx)

        if isinstance(t1, IntTp):
            raise TypecheckingError(f"Expected function, got {t1}")
        elif isinstance(t1, TpVar):  # TpVar ?
            t2 = typecheck_expr(expr.e2, _ctx)

            # e.g. \x. x x
            if t1 == t2:
                raise TypecheckingError(f"Recursive function: {expr}")

            # t1 = t2 -> tnew
            tnew = _ctx._newType()
            _ctx._resolve(t1, Func(t2, tnew))
            return tnew
        else:  # Func
            t2 = typecheck_expr(expr.e2, _ctx)

            # (t1.a -> t1.b) (t2)
            typecheck_app(t1.a, t2, _ctx)

            return t1.b
    elif isinstance(expr, Lam):
        _subctx = _ctx.push()

        _subctx._map[expr.s] = _ctx._newType()
        etype = typecheck_expr(expr.e, _subctx)
        res = Func(_subctx._map[expr.s], etype)

        _ctx = _subctx.pop()
        return res
    else:
        raise TypecheckingError("Unknown expression type")


def typecheck(prog: Prog) -> List[Type]:
    # If there are no type errors, return a list of Types
    # Otherwise, throw TypecheckingError("msg")
    ctx = Context()
    for defn in prog.defns:
        ctx._map[defn.s] = typecheck_expr(defn.e, ctx)
        # print(f"def {defn.s} = {defn.e};  // {ctx._map[defn.s]}")
    return [ctx._map[defn.s] for defn in prog.defns]
