from .VirtualSolver import VirtualSolver
import numpy as np
from .PopulationPool import PopulationPool
from .Translators import PermutationGenotypeTranslator
from copy import copy

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

        self.pop_count = config.get('mi', 20)
        self.breed_count = config.get('lambda', 10)
        self.cross_points = config.get('cross_points', 1)
        self.mutation = config.get('mutation', 0.1) / self.translator.genotype_size
        self.selection = config.get('selection', 'mi_best')  # todo: implement
        self.record = config.get('record', False)  # todo: implement
        self.max_iterations = config.get('max_iterations', 500)
        self.pop_random_seed = config.get('pop_random_seed', None)
        self.random_seed = config.get('random_seed', None)
        self.verbose = config.get('verbose', False)
        self.history = {'pool':[], 'parents':[], 'children':[]}

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
            if self.verbose:
                print("Running {} iteration...".format(iterations))
            if self.record and iterations%self.record == 0:
                self.history['pool'].append(copy(self.gene_pool.pool))
            # 1: Losowanie l elementowa populacje z P - T
            # 2: Reprodukowanie z T l elemenowa populacje potomna krzyzujac i mutujac
            p, c = self.gene_pool.breed(self.breed_count, self.breed_count, self.cross_points, self.mutation)

            if self.record and iterations%self.record == 0:
                self.history['children'].append(copy(c))
                self.history['parents'].append(copy(p))
            # 3: Selekcja mi osobnikow z P+R
            self.gene_pool.kill(self.breed_count, self.selection)
            iterations += 1
        self.result = self.translator.decode(self.gene_pool.get_best())
        self.result = self.translator.get_fenotype(self.result)
        return self.result
