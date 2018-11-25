from .VirtualSolver import VirtualSolver


class DynamicSolver(VirtualSolver):  # dziedziczenie interfejsu, rzecz w pythonie zbedna ale porzadkuje kod

    def nwd(self, a, b):
        while b > 0:
            c = a % b
            a = b
            b = c
        return a

    def solve(self):  # TODO: sprawdzic czy wejscie jest int, jak nie to rzucic wyjatek "Wrong input"
        current_nwd = self.items[0][1]
        for p, w in self.items:
            current_nwd = self.nwd(current_nwd, w)

        backpack = [-1] * (int(self.capacity/current_nwd) + 1)  # symulowana nieskonczonosc
        backpack[0] = 0
        for p, w in self.items:
            pass  # ... algorytm plecakowy uzupelniania plecaka
        return backpack[-1]
