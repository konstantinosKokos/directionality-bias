from random import seed, shuffle
from DirectionalityBias.data.arithm import *
from DirectionalityBias.data.datamaker import sample_dataset

seed(42)

depths, samples_per_depth = list(zip(*[(2, 10), (3, 20), (4, 30), (5, 50), (6, 100),
                                       (7, 100), (8, 200), (9, 50)]))
atom_list = make_atom_list(-10, 11)
op_list = op_list

left_samples = sample_dataset(depths=depths, samples_per_depth=samples_per_depth, atom_list=atom_list,
                              op_list=op_list, directionality='left')
right_samples = sample_dataset(depths=depths, samples_per_depth=samples_per_depth, atom_list=atom_list,
                               op_list=op_list, directionality='right')

left_eval_forward = list(map(lambda expr: arithm_eval_exp(expr, False), left_samples))
left_eval_inverse = list(map(lambda expr: arithm_eval_exp(expr, True), left_samples))

right_eval_forward = list(map(lambda expr: arithm_eval_exp(expr, False), right_samples))
right_eval_inverse = list(map(lambda expr: arithm_eval_exp(expr, True), right_samples))

left_indices = list(range(len(left_samples)))
shuffle(left_indices)
right_indices = list(range(len(right_samples)))
shuffle(right_indices)

left_splitpoint = round(len(left_indices) * 0.8)
right_splitpoint = round(len(right_indices) * 0.8)

left_train = [(left_samples[i], left_eval_forward[i], left_eval_inverse[i])
              for i in left_indices[:left_splitpoint]]
left_val = [(left_samples[i], left_eval_forward[i], left_eval_inverse[i])
            for i in left_indices[left_splitpoint:]]

right_train = [(right_samples[i], right_eval_forward[i], right_eval_inverse[i])
               for i in right_indices[:right_splitpoint]]
right_val = [(right_samples[i], right_eval_forward[i], right_eval_inverse[i])
             for i in right_indices[right_splitpoint:]]
