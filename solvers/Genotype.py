import numpy as np
class Genotype:
    """Generic genotype coding class which can cross and mutate.
    Genes are represented as 0 and 1 characters in a string"""

    def __init__(self, N, code=None):
        self.size = N
        self.code = code or ''.join([str(i) for i in np.random.randint(2, size=self.size)])

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
        locuses = np.random.permutation(self.size)[:k_points]
        locuses.sort()
        locuses += [self.size]
        return [Genotype(self.size, code=code) for code in self._cross(locuses, genotype_other)]

    def _mutate(self, mutations):
        return ''.join([chr(ord(gen) ^ mutacja) for gen, mutacja in zip(self.code, mutations)])

    def mutate(self, chance):
        # wyliczyc pozycje mutacji z rozkladem chance
        # dla kazdego z bitow mutuj wedlug tego rozkladu
        mutations = np.random.random(size = self.size)
        mutations = [i < chance for i in mutations]
        return Genotype(self.size, code=self._mutate(mutations))

    def __eq__(self, other):
        return self.code == other.code

    def __lt__(self, other): # placeholder dla sortowania - nie ma znaczenia
        return self.size < other.size

    def __str__(self):
        return self.code