import unittest
import yaml
from ..solvers.GeneticSolver import GeneticSolver

data = """
description: prize/weight
items:
- !!python/tuple [90, 70]
- !!python/tuple [70, 40]
- !!python/tuple [60, 30]
- !!python/tuple [50, 20]
- !!python/tuple [10, 10]
- !!python/tuple [50, 40]
items_number: 6
capacity: 80
"""

class test_permutation(unittest.TestCase):
    def test_permutation_evaluation(self):
        permutation = [1,5,3,0,2,4]
        test_data = yaml.load(data)
        solver = GeneticSolver(test_data)
        self.assertEqual(solver.evaluate_permutation(permutation), 120)


if __name__ == '__main__':
    unittest.main()
