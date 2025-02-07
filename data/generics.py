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

    def __str__(self) -> str:
        return f'( {str(self.left)} {str(self.op)} {str(self.right)} )'

    def __call__(self) -> str:
        return str(self)

    def __repr__(self) -> str:
        return str(self)

    def polish(self) -> str:
        return f'{str(self.op)} {polish(self.left)} {polish(self.right)}'

    def __len__(self) -> int:
        return get_expr_len(self)


def polish(expr) -> str:
    return expr.polish() if isinstance(expr, Expr) else str(expr)


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


@overload
def flip_expr(expr: LeftExpr[Atom, Op]) -> RightExpr[Atom, Op]:
    pass


@overload
def flip_expr(expr: RightExpr[Atom, Op]) -> LeftExpr[Atom, Op]:
    pass


@overload
def flip_expr(expr: Atom) -> Atom:
    pass


def flip_expr(expr):
    if isinstance(expr, LeftExpr):
        return RightExpr(left=expr.right, right=flip_expr(expr.left), op=expr.op)
    elif isinstance(expr, RightExpr):
        return LeftExpr(left=flip_expr(expr.right), right=expr.left, op=expr.op)
    else:
        return expr


def sample_left_expr(depth: int, atoms: Atoms, ops: Ops) -> Union[LeftExpr[Atom, Op], Atom]:
    if depth == 0:
        return sample(atoms)
    else:
        return LeftExpr(left=sample_left_expr(depth=depth - 1, atoms=atoms, ops=ops),
                        right=sample(atoms),
                        op=sample(ops))


def sample_right_expr(depth: int, atoms: Atoms, ops: Ops) -> Union[RightExpr[Atom, Op], Atom]:
    if depth == 0:
        return sample(atoms)
    else:
        return RightExpr(left=sample(atoms),
                         right=sample_right_expr(depth=depth-1, atoms=atoms, ops=ops),
                         op=sample(ops))


def sample(choices: List[Something]) -> Something:
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
    if isinstance(expr, LeftExpr):
        return eval_lexp(expr, atom_semantics, op_semantics)
    elif isinstance(expr, RightExpr):
        return eval_rexp(expr, atom_semantics, op_semantics)
    else:
        return atom_semantics(expr)

def get_expr_len(expr: Union[Atom, Expr]) -> int:
    if isinstance(expr, Expr):
        return max(get_expr_len(expr.left), get_expr_len(expr.right)) + 1
    else:
        return 1