from DirectionalityBias.data.generics import *
from operator import add, sub


def atom_semantics(atom: str) -> int:
    return int(atom)


operator_semantics: Mapping[str, Callable[[int, int], int]] = {'+': add, '-': sub}
op_list = list(operator_semantics.keys())


ArithLeftExpr = LeftExpr[str, str]
ArithRightExpr = RightExpr[str, str]


def make_atom_list(low: int, high: int) -> List[str]:
    return [str(i) for i in range(low, high)]


def arithm_eval_exp(exp: Expr) -> int:
    return eval_exp(exp, atom_semantics, operator_semantics)
