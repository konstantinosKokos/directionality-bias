from DirectionalityBias.data.generics import *
from itertools import chain


def sample_dataset(depths: List[int], atom_list: List[Atom], op_list: List[Op], samples_per_depth: List[int],
                   directionality: str, enforce_unique: bool = False) -> List[Expr]:
    """
        Randomly samples a number of expressions according to the parameters specified.

    :param depths:  A list of ints, specifying the branching depths of the random expressions to be generated.
    :param atom_list: A list of atomic primitives used for the expression generation.
    :param op_list: A list of binary operator symbols used for the expression generation.
    :param samples_per_depth: A list of ints, specifying the number of samples to be generated at each depth.
    :param directionality: A string, either "left" or "right".
    :param enforce_unique: Bool, defaults to False. Set to True if you want to disallow repetition of samples.
    :return: A list of expressions
    """

    if directionality == 'left':
        gen = sample_left_expr
    elif directionality == 'right':
        gen = sample_left_expr
    else:
        raise ValueError('Argument directionality must be one of ("right", left")')
    if enforce_unique:
        post_proc = set
    else:
        post_proc = lambda x: x
    return list(chain.from_iterable([
        post_proc([gen(depth, atom_list, op_list) for _ in range(numsamples)])
        for depth, numsamples in zip(depths, samples_per_depth)]))
