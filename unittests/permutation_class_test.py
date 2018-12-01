import unittest
from ..solvers.GeneticSolver import PermutationFenotype, Genotype


class test_permutation(unittest.TestCase):
    def test_decode(self):
        input = Genotype(7, "01001100001011")
        expected_result = [1,5,3,6,0,2,4]
        permutation = PermutationFenotype.decode(input)
        self.assertListEqual(permutation, expected_result)

        # def mutate(self, chance):
        #     # wyliczyc pozycje mutacji z rozkladem chance
        #     # dla kazdego z bitow mutuj wedlug tego rozkladu
        #     mutations = np.random.random(size=self.real_size)
        #     mutations = [i >= chance for i in mutations]
        #     return ''.join([chr(ord(gen) ^ mutacja) for gen, mutacja in zip(self.code, mutations)])

    def test_mutate_statistic(self):
        sample_genotype = Genotype(7, "01001100001011")
        mutate_chance = 0.1
        mutation_counter = 0
        samples = 1000
        expected_mutations = samples * sample_genotype.real_size * mutate_chance
        possible_mutations = samples * sample_genotype.real_size
        def count_mutations(gtype):
            return sum([sg != gt for sg, gt in zip(sample_genotype.code, gtype)])
        for i in range(samples):
            mutated = sample_genotype.mutate(chance=mutate_chance)
            mutation_counter += count_mutations(mutated)
        self.assertAlmostEqual(expected_mutations/possible_mutations, mutation_counter/possible_mutations, 1)


if __name__ == '__main__':
    unittest.main()
