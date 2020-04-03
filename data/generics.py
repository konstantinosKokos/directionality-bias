from typing import *
from random import choice
from abc import abstractmethod

Atom = TypeVar('Atom')
Op = TypeVar('Op')
Domain = TypeVar('Domain')
Something = TypeVar('Something')

Atoms = List[Atom]
Ops = List[Op]


class Expr:
    @abstractmethod
    def __init__(self):
        pass

    def __str__(self):
        return f'( {str(self.left)} {str(self.op)} {str(self.right)} )'

    def __call__(self):
        return str(self)

    def __repr__(self):
        return str(self)

    def polish(self) -> str:
        return f'{str(self.op)} {polish(self.left)} {polish(self.right)}'


def polish(expr) -> str:
    return expr.polish() if isinstance(expr, Expr) else str(expr)


class BinaryLeftExpr(Expr, Generic[Atom, Op]):
    def __init__(self, left: Union[Atom, 'BinaryLeftExpr'], right: Atom, op: Op) -> None:
        super(BinaryLeftExpr, self).__init__()
        self.left = left
        self.right = right
        self.op = op


class BinaryRightExpr(Expr, Generic[Atom, Op]):
    def __init__(self, left: Atom, right: Union[Atom, 'BinaryRightExpr'], op: Op) -> None:
        super(BinaryRightExpr, self).__init__()
        self.left = left
        self.right = right
        self.op = op


@overload
def flip_expr(expr: BinaryLeftExpr[Atom, Op]) -> BinaryRightExpr[Atom, Op]:
    pass


@overload
def flip_expr(expr: BinaryRightExpr[Atom, Op]) -> BinaryLeftExpr[Atom, Op]:
    pass


@overload
def flip_expr(expr: Atom) -> Atom:
    pass


def flip_expr(expr):
    if isinstance(expr, BinaryLeftExpr):
        return BinaryRightExpr(left=expr.right, right=flip_expr(expr.left), op=expr.op)
    elif isinstance(expr, BinaryRightExpr):
        return BinaryLeftExpr(left=flip_expr(expr.right), right=expr.left, op=expr.op)
    else:
        return expr


def sample_left_expr(depth: int, atoms: Atoms, ops: Ops) -> Union[BinaryLeftExpr[Atom, Op], Atom]:
    if depth == 0:
        return sample(atoms)
    else:
        return BinaryLeftExpr(left=sample_left_expr(depth=depth - 1, atoms=atoms, ops=ops),
                              right=sample(atoms),
                              op=sample(ops))


def sample_right_expr(depth: int, atoms: Atoms, ops: Ops) -> Union[BinaryRightExpr[Atom, Op], Atom]:
    if depth == 0:
        return sample(atoms)
    else:
        return BinaryRightExpr(left=sample(atoms),
                               right=sample_right_expr(depth=depth-1, atoms=atoms, ops=ops),
                               op=sample(ops))


def sample(choices: List[Something]) -> Something:
    return choice(choices)


def eval_lexp(expr: Union[Atom, BinaryLeftExpr],
              atom_semantics: Callable[[Atom], Domain],
              op_semantics: Mapping[Op, Callable[[Domain, Domain], Domain]]) -> Domain:
    if isinstance(expr, BinaryLeftExpr):
        return op_semantics[expr.op](eval_lexp(expr.left, atom_semantics, op_semantics), atom_semantics(expr.right))
    else:
        return atom_semantics(expr)


def eval_rexp(expr: Union[Atom, BinaryRightExpr],
              atom_semantics: Callable[[Atom], Domain],
              op_semantics: Mapping[Op, Callable[[Domain, Domain], Domain]]) -> Domain:
    if isinstance(expr, BinaryRightExpr):
        return op_semantics[expr.op](atom_semantics(expr.left),
                                     eval_rexp(expr.right, atom_semantics, op_semantics))
    else:
        return atom_semantics(expr)


def eval_exp(expr: Union[Atom, Expr],
             atom_semantics: Callable[[Atom], Domain],
             op_semantics: Mapping[Op, Callable[[Domain, Domain], Domain]],
             invert: bool = False) -> Domain:
    if invert:
        expr = flip_expr(expr)
    if isinstance(expr, BinaryLeftExpr):
        return eval_lexp(expr, atom_semantics, op_semantics)
    elif isinstance(expr, BinaryRightExpr):
        return eval_rexp(expr, atom_semantics, op_semantics)
    else:
        return atom_semantics(expr)
