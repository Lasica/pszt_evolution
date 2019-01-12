from .VirtualSolver import VirtualSolver
import numpy as np
import operator

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
# todo: napisac inne translatory i inne reprezentacje: np. zbiorowy albo inna reprezentacje permutacji (wagowa?)
class PermutationGenotypeTranslator:
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
    def __init__(self, size, cap, items):
        self.size = size
        self.genotype_size = PermutationGenotypeTranslator._calculate_genotype_length(size)
        self.capacity = cap
        self.items = items

    @staticmethod
    def decode(genotype):
        """Decodes genotype and returns fenotype - permutation that dictates order
        in which items are to be taken in greedy manner"""
        permutation = [0]
        sum_i = 0
        nbit = 1
        i = 1
        while sum_i < genotype.size:
            #print(i, nbit, ' ({} {}) {}'.format(sum_i, sum_i + nbit, f[sum_i:sum_i + nbit]))
            index = int(genotype.code[sum_i:sum_i + nbit], 2) % (i+1)
            permutation.insert(index, i)
            sum_i += nbit
            if i + 1 >= (1 << nbit):
                nbit += 1
            i += 1
        return permutation

    def evaluate_fenotype(self, permutation): # permutacja - lista liczb
        box = self.capacity
        value = 0
        for i in permutation:
            if box >= self.items[i][1]:
                value += self.items[i][0]
                box -= self.items[i][1]
            if box <= 0:
                break
        return value

    def decode_and_evaluate(self, genotype):
        return self.evaluate_fenotype(PermutationGenotypeTranslator.decode(genotype))

    def get_fenotype(self, permutation):
        box = self.capacity
        taken = []
        for i in permutation:
            if box >= self.items[i][1]:
                taken.append(self.items[i])
                box -= self.items[i][1]
            if box <= 0:
                break
        return taken

    @staticmethod
    def _calculate_genotype_length(size):
        """Returns number of bits that permutation encoding requires"""
        total_size = 0
        s = 1  # pozycja kodowania n-tego bitu w genie
        for n_bit in range(20):
            total_size += (size - s)
            s *= 2
            if s > size:
                break

        return total_size


class PopulationPool:
    def __init__(self, pool_size, translator):
        self.translator = translator
        self.pool_size  = pool_size
        self.pool       = [] # pary wartosci (score, genome) (wynik genotypu) na podstawie ktorego obliczane jest fitness

    def spawn_random(self, pop_count):
        """Spawns pop_count random genomes and adds them to the pool - used for initialisation"""
        temporarypool = [Genotype(self.translator.genotype_size) for _ in range(pop_count)]
        temporarypool = [(self.translator.decode_and_evaluate(genome), genome) for genome in temporarypool]
        self.pool    += temporarypool

    # do napisania funkcje:
    def select_parents(self, parent_count):  # zwyczajowo breed_count == parent_count
        parents = np.random.choice(range(len(self.pool)), parent_count, replace=False)
        return parents

    def breed(self, parent_count, breed_count, cross_points, mutation_chance):
        # breed - reprodukuje breed_count osobnikow na podstawie rodzicow i dodaje ich do pool (obliczajac wyniki genomow)
        # wola select_parents

        parents = self.select_parents(parent_count)  # indeksy
        while breed_count:
            parent_pair = np.random.choice(parents, 2, replace=False)
            genomA, genomB = self.pool[parent_pair[0]][1], self.pool[parent_pair[1]][1]

            children = genomA.cross(genomB, cross_points)
            children = [child.mutate(mutation_chance) for child in children]
            children = [(self.translator.decode_and_evaluate(genotype), genotype)for genotype in children]
            self.pool += children
            breed_count -= 2


    def _calculate_normalised_fitness(self, selection_pressure=1):
        # dla metody ruletki liczy prawdopodobienstwa
        # liczy srednia i wariancje z wartosci score i zwraca exp(scores) jako fitness - pstwo przezywalnosci
        scores = np.array([gs[0] for gs in self.pool])
        mean = scores.mean()
        stdev = np.sqrt(np.dot(scores,scores)/scores.size - mean**2)  # wariancja policzona szybko
        scores = (scores - mean)*selection_pressure/stdev
        return np.exp(scores)

    def _randomise_with_weights(self, count, survivability): # count == kill_count albo losujemy kto przezyl;
        prefix_sum = np.cumsum(survivability)
        return [np.searchsorted(prefix_sum, r) for r in
                     np.random.random(count)*prefix_sum[-1]]
        # funkcja pomocnicza do wyznaczenia
        pass

    def get_best(self):
    # zwraca genom najlepszego osobnika z populacji wzgledem wartosci score - na koniec zeby zdekodowac i miec wynik
        self.pool.sort(reverse=True)
        return self.pool[0][1]

    def kill(self, kill_count, selection_method='mi_best'):
        """Losowanie ze zwracaniem - zabija kill_count osobnikow z populacji zgodnie z wybrana metoda selekcji:
            selection_method=
                'mi_best' - zabija kill_count najgorszych osobnikow
                'roulette' - rozklad zabitych osobnikow jest zgodny ze znormalizowana funkcja przystosowania exp(fnorm())
                'ranking' - rozkład zabitych osobników jest zgodny z rankingiem wyników genotypów"""
        # ruletka - _calculate_normalised_fitness DONE
        # rankingowa - liczy pstwa na podstawie rankingu
        # mi_best - zabija ostatnich kill_count DONE
        leftovers = len(self.pool)-kill_count
        self.pool.sort(reverse=True)
        if (selection_method == "ranking"):
            survivability = np.cumsum(np.arange(start=len(self.pool)), stop=0, step=-1)
            survivors = self._randomise_with_weights(leftovers, survivability)
            self.pool = [self.pool[i] for i in survivors]

        elif (selection_method == "roulette"):
            survivability = self._calculate_normalised_fitness()
            survivors = self._randomise_with_weights(leftovers, survivability)
            self.pool = [self.pool[i] for i in survivors]

        elif (selection_method == "mi_best"):
            self.pool = self.pool[:leftovers]

class GeneticSolver(VirtualSolver):
    """Config:
        record      - zapisuje co k-ty posredni krok ewolucyjny do narysowania wykresu przebiegu
        selection   - metoda ruletki, rankingowa, u najlepszych | normalizacja funkcji przystoswania
        cross_points - liczba punktow w krzyzowaniu od 1 do N-1
        mutation    - prawdopodobienstwo mutacji pojedynczego genu w genotypie
            wartosc 0.1 oznacza ze srednio 1 na 10 genotypow bedzie mial 1 mutacje
        mi          - parametr mi - licznosc populacji
        lambda      - parametr lambda - licznosc potomstwa
        translator  - wybiera jaki wariant reprezentacji kodu genetycznego uzyc
        pop_random_seed - ziarno do losowania populacji
        random_seed - ziarno do symulacji - powinno byc ustawione gdy ziarno populacji tez jest ustawione"""
    def __init__(self, data, config=None):
        VirtualSolver.__init__(self, data, config)
        if config.get('translator', 'permutation') == 'permutation':
            self.translator = PermutationGenotypeTranslator(len(self.items), self.capacity, self.items)
        else:
            raise Exception("Unknown translator configuration {}".format(self.translator))

        self.pop_count      = config.get('mi', 20)
        self.breed_count    = config.get('lambda', 10)
        self.cross_points   = config.get('cross_points', 1)
        self.mutation       = config.get('mutation', 0.1) / self.translator.genotype_size
        self.selection      = config.get('selection', 'mi_best') # todo: implement
        self.record         = config.get('record', False)   # todo: implement
        self.max_iterations = config.get('max_iterations', 500)
        self.pop_random_seed=config.get('pop_random_seed', None)
        self.random_seed    =config.get('random_seed', None)


    def init_genepool(self):
        np.random.seed(self.pop_random_seed)
        self.gene_pool = PopulationPool(self.pop_count, self.translator)
        self.gene_pool.spawn_random(self.pop_count)
        np.random.seed(self.random_seed)

    def solve(self):
        # 0: Wygenerowac mi osobnikow do populacji P
        self.init_genepool()
        # 4: stop jesli warunek stopu - liczba iteracji algorytmu (~500) lub % najlepszego wyniku (~90%?)
        iterations = 0
        while iterations < self.max_iterations:
            print("Running {} iteration...".format(iterations))
            # 1: Losowanie l elementowa populacje z P - T
            # 2: Reprodukowanie z T l elemenowa populacje potomna krzyzujac i mutujac
            self.gene_pool.breed(self.breed_count, self.breed_count,  self.cross_points, self.mutation)
            # 3: Selekcja mi osobnikow z P+R
            self.gene_pool.kill(self.breed_count, self.selection)
            iterations += 1
        self.result = self.translator.decode(self.gene_pool.get_best())
        self.result = self.translator.get_fenotype(self.result)
        return self.result
