from .VirtualSolver import VirtualSolver


class GreedySolver(VirtualSolver):  # dziedziczenie interfejsu, rzecz w pythonie zbedna ale porzadkuje kod

    def solve(self):
        items = [(i, item[0], item[1]) for i, item in enumerate(self.items)]
        items.sort(reverse=True, key=lambda x: x[1])
        taken = 0
        for i, p, w in items:
            if taken + w < self.capacity:
                self.result.append(((p, w), i))
                taken += w