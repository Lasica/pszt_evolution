from .Genotype import Genotype
import numpy as np


class PopulationPool:
    def __init__(self, pool_size, translator):
        self.translator = translator
        self.pool_size = pool_size
        self.pool = []  # pary wartosci (score, genome) (wynik genotypu) na podstawie ktorego obliczane jest fitness

    def breed(self, parent_count, breed_count, cross_points, mutation_chance):
        # breed - reprodukuje breed_count osobnikow na podstawie rodzicow i dodaje ich do pool (obliczajac wyniki genomow)
        # wola select_parents

        parents = self._select_parents(parent_count)  # indeksy
        while breed_count:
            parent_pair = np.random.choice(parents, 2, replace=False)
            genomA, genomB = self.pool[parent_pair[0]][1], self.pool[parent_pair[1]][1]

            children = genomA.cross(genomB, cross_points)
            children = [child.mutate(mutation_chance) for child in children]
            children = [(self.translator.decode_and_evaluate(genotype), genotype) for genotype in children]
            self.pool += children
            breed_count -= 2
        return parents, children

    def get_best(self):
        # zwraca genom najlepszego osobnika z populacji wzgledem wartosci score - na koniec zeby zdekodowac i miec wynik
        self.pool.sort(reverse=True)
        return self.pool[0][1]

    def kill(self, kill_count, selection_method='mi_best', selection_pressure = 0.5):
        """Losowanie ze zwracaniem - zabija kill_count osobnikow z populacji zgodnie z wybrana metoda selekcji:
            selection_method=
                'mi_best' - zabija kill_count najgorszych osobnikow
                'roulette' - rozklad zabitych osobnikow jest zgodny ze znormalizowana funkcja przystosowania exp(fnorm())
                'ranking' - rozkład zabitych osobników jest zgodny z rankingiem wyników genotypów"""
        # ruletka - _calculate_normalised_fitness DONE
        # rankingowa - liczy pstwa na podstawie rankingu
        # mi_best - zabija ostatnich kill_count DONE
        leftovers = len(self.pool) - kill_count
        self.pool.sort(reverse=True)
        if (selection_method == "ranking"):
            survivability = np.arange(stop=0, start=len(self.pool), step=-1)
            survivors = self._randomise_with_weights(leftovers, survivability)
            self.pool = [self.pool[i] for i in survivors]

        elif (selection_method == "roulette"):
            survivability = self._calculate_normalised_fitness(selection_pressure)
            survivors = self._randomise_with_weights(leftovers, survivability)
            self.pool = [self.pool[i] for i in survivors]

        elif (selection_method == "roulette_no_return"):
            survivability = self._calculate_normalised_fitness(selection_pressure)
            surv_sum = sum(survivability)
            survivability /= surv_sum
            survivors = np.random.choice(len(survivability), leftovers, replace=False, p=survivability)
            self.pool = [self.pool[i] for i in survivors]

        elif (selection_method == "ranking_no_return"):
            survivability = np.arange(stop=0, start=len(self.pool), step=-1, dtype=float)
            surv_sum = sum(survivability)
            survivability /= surv_sum
            survivors = np.random.choice(len(survivability), leftovers, replace=False, p=survivability)
            self.pool = [self.pool[i] for i in survivors]

        elif (selection_method == "mi_best"):
            self.pool = self.pool[:leftovers]

        else:
            raise Exception("Unknown selection method")

    def spawn_random(self, pop_count):
        """Spawns pop_count random genomes and adds them to the pool - used for initialisation"""
        temporarypool = [Genotype(self.translator.genotype_size) for _ in range(pop_count)]
        temporarypool = [(self.translator.decode_and_evaluate(genome), genome) for genome in temporarypool]
        self.pool += temporarypool

    def _calculate_normalised_fitness(self, selection_pressure=0.5):
        # dla metody ruletki liczy prawdopodobienstwa
        # liczy srednia i wariancje z wartosci score i zwraca exp(scores) jako fitness - pstwo przezywalnosci
        scores = np.array([gs[0] for gs in self.pool])
        mean = scores.mean()
        stdev = np.sqrt(np.dot(scores, scores) / scores.size - mean ** 2)  # wariancja policzona szybko
        if stdev:
            scores = (scores - mean) * selection_pressure / stdev
            return np.exp(scores)
        else:
            return np.ones(scores.shape)


    def _randomise_with_weights(self, count, survivability):  # count == kill_count albo losujemy kto przezyl;
        prefix_sum = np.cumsum(survivability)
        return [np.searchsorted(prefix_sum, r) for r in
                np.random.random(count) * prefix_sum[-1]]
        # funkcja pomocnicza do wyznaczenia
        pass

    def _select_parents(self, parent_count):  # zwyczajowo breed_count == parent_count
        parents = np.random.choice(range(len(self.pool)), parent_count, replace=False)
        return parents
