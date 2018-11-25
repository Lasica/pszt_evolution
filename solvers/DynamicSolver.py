from .VirtualSolver import VirtualSolver


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
        backpack = [(-1, -1)] * (backpack_slots + 1)  # symulowana nieskonczonosc
        backpack[0] = (0, -1)
        for j, item in enumerate(self.items):  # petla po dostepnych przedmiotach
            p = item[0]
            w = item[1]
            for i in reversed(range(len(backpack))):  # petla po miejscach w w plecaku (od tylu)
                if i + w/current_nwd <= backpack_slots and backpack[i][0] > -1:
                    if backpack[i + int(w/current_nwd)][0] < backpack[i][0] + p:
                        backpack[i + int(w/current_nwd)] = (backpack[i][0] + p, j)

        # odtwarzanie wyniku
        self.result = []
        prize = max(backpack)
        best_idx = backpack.index(prize)
        while prize[0] > 0:
            item = self.items[prize[1]]
            self.result.append((item, prize[1]))
            best_idx = best_idx - int(item[1]/current_nwd)
            prize = backpack[best_idx]
        return
