from .VirtualSolver import VirtualSolver
import numpy as np

class Genotype:

    def __init__(self, N, code=None):
        self.size = N
        self.real_size = self.get_format(N)
        if not code:
            self.code = ''.join([str(i) for i in np.random.randint(2, size=self.real_size)])
        else:
            self.code = code  # uzywac rozwaznie

    @staticmethod
    def get_format(size):
        total_size = 0
        s = 1
        for i in range(20):
            total_size += i * (size - s)
            s *= 2
            if s > size:
                break
        return total_size

    def _cross(self, positions, genotype_other):
        children = ["", ""]
        prev_locus = 0
        gtyp1, gtyp2 = genotype_other.code, self.code
        for locus in positions:
            gtyp1, gtyp2 = gtyp2, gtyp1
            children[0] += gtyp1[prev_locus:locus]
            children[1] += gtyp2[prev_locus:locus]
            prev_locus = locus
        return children

    def cross(self, genotype_other, k_points):  # k_points <= format -1
        locuses = np.random.permutation(self.real_size)[:k_points]
        locuses.sort()
        locuses += [self.real_size]
        return self._cross(locuses, genotype_other)

    def _mutate(self, mutations):
        return ''.join([chr(ord(gen) ^ mutacja) for gen, mutacja in zip(self.code, mutations)])

    def mutate(self, chance):
        # wyliczyc pozycje mutacji z rozkladem chance
        # dla kazdego z bitow mutuj wedlug tego rozkladu
        mutations = np.random.random(size = self.real_size)
        mutations = [i < chance for i in mutations]
        return self._mutate(mutations)

class PermutationFenotype:

    @staticmethod
    def decode(genotype):
        permutation = [0]
        sum_i = 0
        nbit = 1
        for i in range(1,   genotype.size):
            #print(i, nbit, ' ({} {}) {}'.format(sum_i, sum_i + nbit, f[sum_i:sum_i + nbit]))
            index = int(genotype.code[sum_i:sum_i + nbit], 2) % (i+1)
            permutation.insert(index, i)
            sum_i += nbit
            if i + 1 >= (1 << nbit):
                nbit += 1
        return permutation

    # @classmethod
    # def code(cls, permutation):
    #     genotype =
    #     return genotype  # bit representation of total_size length
    #
    # @classmethod
    # def random_permutation(cls, N):
    #     return np.random.permutation(N)


class GeneticSolver(VirtualSolver):
    def __init__(self, data, config):
        VirtualSolver.__init__(self, data, config)
        self.translator = config['translator']

    def solve(self):
        # placeholder, funkcja powinna zwracać wynik (wartosc, upakowanie plecaka);
        # dokladne przedmioty uzyte do upakowania powinny byc w self.result
        return self.result
