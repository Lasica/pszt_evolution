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
            # print(i, nbit, ' ({} {}) {}'.format(sum_i, sum_i + nbit, f[sum_i:sum_i + nbit]))
            index = int(genotype.code[sum_i:sum_i + nbit], 2) % (i + 1)
            permutation.insert(index, i)
            sum_i += nbit
            if i + 1 >= (1 << nbit):
                nbit += 1
            i += 1
        return permutation

    def evaluate_fenotype(self, permutation):  # permutacja - lista liczb
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
                taken.append((self.items[i], i))
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
