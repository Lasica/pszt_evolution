from .VirtualSolver import VirtualSolver
import numpy as np

class Genotype:
    """Encodes permutation in the following fashion:
    Subsequent numbers are bits encoding position (looped with modulo using current position numbers)
    Clusters of bits represent number that encodes the position into which insert the position in permutation
    Example:
        bits: 0|10|11|000|111 codes:
        step 0: 0
        step 1: 1 0         <- bits: "0b, 0" inserting "1" into 0 position
        step 2: 1 0 2       <- bits: "10b, 2" inserting "2" into 2 position
        step 3: 1 0 2 3     <- bits: "11b, 3" inserting "3" into 3 position
        step 4: 4 1 0 2 3   <- bits: "000b, 0" inserting "4" into 0 position
        step 5: 4 1 5 0 2 3 <- bits: "111b, 7" inserting "5" into 7%5=2 position
        """

    def __init__(self, N, code=None):
        self.size = N
        self.real_size = self.get_format(N)
        if not code:
            self.code = ''.join([str(i) for i in np.random.randint(2, size=self.real_size)])
        else:
            self.code = code  # uzywac rozwaznie

    @staticmethod
    def get_format(size):
        """Returns number of bits that permutation encoding really requires"""
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
        """Problem: funkcja dziala wolno przez wiele insertow (N^2)"""
        permutation = [0]
        sum_i = 0
        nbit = 1
        for i in range(1, genotype.size):
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
    """Config:
        record - zapisuje co k-ty posredni krok ewolucyjny do narysowania wykresu przebiegu
        selection - metoda ruletki, rankingowa, u najlepszych | normalizacja funkcji przystoswania
        cross - liczba punktow w krzyzowaniu od 1 do N-1
        mutation - prawdopodobienstwo mutacji"""
    def __init__(self, data, config=None): # todo: dodac config
        VirtualSolver.__init__(self, data, config)
        # self.translator = config['translator']

    def evaluate_permutation(self, permutation): # permutacja - lista liczb
        box = self.capacity
        value = 0
        for i in permutation:
            if box >= self.items[i][1]:
                value += self.items[i][0]
                box -= self.items[i][1]
            if box <= 0:
                break
        return value

    def solve(self):
        # config:
        # placeholder, funkcja powinna zwracać wynik (wartosc, upakowanie plecaka);
        # dokladne przedmioty uzyte do upakowania powinny byc w self.result
        # 0: Wygenerowac u osobnikow do populacji P
        # 1: Losowanie l elementowa populacje z P - T
        # 2: Reprodukowanie z T l elemenowa populacje potomna krzyzujac i mutujac
        # 3: Selekcja u osobnikow z P+R
        # 4: stop jesli warunek stopu
        return self.result
