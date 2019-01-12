from .VirtualSolver import VirtualSolver
import numpy as np


class DynamicSolver(VirtualSolver):  # dziedziczenie interfejsu, rzecz w pythonie zbedna ale porzadkuje kod

    def nwd(self, a, b):
        while b > 0:
            c = a % b
            a = b
            b = c
        return a

    def solve(self):
        if not (type(self.items[0][0]) is int and type(self.items[0][1]) is int):
            raise Exception("Wrong input type. Should be int, while it is {} {}".format(type(self.items[0][0]), type(self.items[0][1])))

        current_nwd = self.items[0][1]  # przechowywanie pierwszego elementu tablicy
        for p, w in self.items:  #petla sluzaca do wyznaczania nwd
            current_nwd = self.nwd(current_nwd, w)

        backpack_slots = int(self.capacity/current_nwd)
        backpack = [-1] * (backpack_slots + 1)  # symulowana nieskonczonosc
        taken = np.zeros((len(self.items), backpack_slots+1), dtype='uint8')
        backpack[0] = 0
        for j, item in enumerate(self.items):  # petla po dostepnych przedmiotach
            p, w = item
            for i in reversed(range(len(backpack))):  # petla po miejscach w w plecaku (od tylu)
                if i + w/current_nwd <= backpack_slots and backpack[i] > -1:
                    nidx = i+int(w/current_nwd)
                    if backpack[nidx] < backpack[i] + p:
                        backpack[nidx] = backpack[i] + p
                        taken[j][nidx] = 1

        # odtwarzanie wyniku
        self.result = []
        prize = max(backpack)
        best_idx = backpack.index(prize)
        first_taken = len(self.items)
        while prize > 0:
            first_taken -= 1
            while not taken[first_taken][best_idx]:
                first_taken -= 1
            item = self.items[first_taken]
            self.result.append((item, first_taken))
            best_idx = best_idx - int(item[1]/current_nwd)
            prize = backpack[best_idx]
        return
