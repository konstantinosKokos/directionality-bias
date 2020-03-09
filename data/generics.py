from typing import *
from random import choice
from abc import abstractmethod

Atom = TypeVar('Atom')
Op = TypeVar('Op')
Domain = TypeVar('Domain')


class Expr:
    @abstractmethod
    def __init__(self):
        pass

    def __str__(self):
        return f'({str(self.left)} {str(self.op)} {str(self.right)})'

    def __call__(self):
        return str(self)

    def __repr__(self):
        return str(self)


class LeftExpr(Expr, Generic[Atom, Op]):
    def __init__(self, left: Union[Atom, 'LeftExpr'], right: Atom, op: Op) -> None:
        super(LeftExpr, self).__init__()
        self.left = left
        self.right = right
        self.op = op


class RightExpr(Expr, Generic[Atom, Op]):
    def __init__(self, left: Atom, right: Union[Atom, 'RightExpr'], op: Op) -> None:
        super(RightExpr, self).__init__()
        self.left = left
        self.right = right
        self.op = op


def sample_left_expr(depth: int, atoms: List[Atom], ops: List[Op]) -> Union[LeftExpr[Atom, Op], Atom]:
    if depth == 0:
        return sample(atoms)
    else:
        return LeftExpr(left=sample_left_expr(depth=depth-1, atoms=atoms, ops=ops),
                        right=sample(atoms),
                        op=sample(ops))


def sample_right_expr(depth: int, atoms: List[Atom], ops: List[Op]) -> Union[RightExpr[Atom, Op], Atom]:
    if depth == 0:
        return sample(atoms)
    else:
        return RightExpr(left=sample(atoms),
                         right=sample_right_expr(depth=depth-1, atoms=atoms, ops=ops),
                         op=sample(ops))


def sample(choices: List[Domain]) -> Domain:
    return choice(choices)


def eval_lexp(expr: Union[Atom, LeftExpr],
              atom_semantics: Callable[[Atom], Domain],
              op_semantics: Mapping[Op, Callable[[Domain, Domain], Domain]]) -> Domain:
    if isinstance(expr, LeftExpr):
        return op_semantics[expr.op](eval_lexp(expr.left, atom_semantics, op_semantics), atom_semantics(expr.right))
    else:
        return atom_semantics(expr)


def eval_rexp(expr: Union[Atom, RightExpr],
              atom_semantics: Callable[[Atom], Domain],
              op_semantics: Mapping[Op, Callable[[Domain, Domain], Domain]]) -> Domain:
    if isinstance(expr, RightExpr):
        return op_semantics[expr.op](atom_semantics(expr.right), eval_rexp(expr.left, atom_semantics, op_semantics))
    else:
        return atom_semantics(expr)


def eval_exp(expr: Union[Atom, Expr],
             atom_semantics: Callable[[Atom], Domain],
             op_semantics: Mapping[Op, Callable[[Domain, Domain], Domain]]):
    if isinstance(expr, LeftExpr):
        return eval_lexp(expr, atom_semantics, op_semantics)
    elif isinstance(expr, RightExpr):
        return eval_rexp(expr, atom_semantics, op_semantics)
    else:
        return atom_semantics(expr)