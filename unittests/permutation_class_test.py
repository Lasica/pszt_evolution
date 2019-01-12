import unittest
from ..solvers.GeneticSolver import Genotype, PermutationGenotypeTranslator
import numpy as np


class test_permutation(unittest.TestCase):
    def test_decode(self):
        input = Genotype(14, "01001100001011")
        expected_result = [1,5,3,6,0,2,4]
        permutation = PermutationGenotypeTranslator.decode(input)
        self.assertListEqual(permutation, expected_result)

    def test_genotype_length(self):
        self.assertEqual(PermutationGenotypeTranslator._calculate_genotype_length(1), 0)
        # self.assertEqual(PermutationGenotypeTranslator._calculate_genotype_length(2), 1)
        self.assertEqual(PermutationGenotypeTranslator._calculate_genotype_length(3), 3)
        self.assertEqual(PermutationGenotypeTranslator._calculate_genotype_length(4), 5)
        self.assertEqual(PermutationGenotypeTranslator._calculate_genotype_length(5), 8)
        self.assertEqual(PermutationGenotypeTranslator._calculate_genotype_length(6), 11)
        self.assertEqual(PermutationGenotypeTranslator._calculate_genotype_length(7), 14)
        self.assertEqual(PermutationGenotypeTranslator._calculate_genotype_length(8), 17)
        self.assertEqual(PermutationGenotypeTranslator._calculate_genotype_length(9), 21)
        self.assertEqual(PermutationGenotypeTranslator._calculate_genotype_length(20), 69)
        # def mutate(self, chance):
        #     # wyliczyc pozycje mutacji z rozkladem chance
        #     # dla kazdego z bitow mutuj wedlug tego rozkladu
        #     mutations = np.random.random(size=self.size)
        #     mutations = [i >= chance for i in mutations]
        #     return ''.join([chr(ord(gen) ^ mutacja) for gen, mutacja in zip(self.code, mutations)])

    def test_mutate_statistic(self):
        sample_genotype = Genotype(14, "01001100001011")
        mutate_chance = 0.1
        mutation_counter = 0
        samples = 1000
        expected_mutations = samples * sample_genotype.size * mutate_chance
        possible_mutations = samples * sample_genotype.size
        def count_mutations(gtype):
            return sum([sg != gt for sg, gt in zip(sample_genotype.code, gtype.code)])
        for i in range(samples):
            mutated = sample_genotype.mutate(chance=mutate_chance)
            mutation_counter += count_mutations(mutated)
        self.assertAlmostEqual(expected_mutations/possible_mutations, mutation_counter/possible_mutations, 1)

    def test_mutate_basic(self):
        sample_genotype = Genotype(14, "01001100001011")
        other_genotype = Genotype(14, sample_genotype._mutate([1]*sample_genotype.size))
        self.assertEqual(other_genotype.code, "10110011110100")

    def test_cross_basic(self):
        sample_genotype = Genotype(14,"11111111111111") #4, 7
        other_genotype = Genotype(14, "00000000000000")
        ###############################012345678901234
        expected_crossed =           ["00001110000000",
                                      "11110001111111"]
        self.assertCountEqual(expected_crossed, sample_genotype._cross([4,7,sample_genotype.size], other_genotype))
        # self.assertCountEqual(expected_crossed, ["00000000000000", "11111111111111"])  # zwraca falsz



if __name__ == '__main__':
    unittest.main()
