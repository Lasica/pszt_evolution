from solvers.GreedySolver import GreedySolver
from solvers.DynamicSolver import DynamicSolver
from solvers.SmartGreedySolver import SmartGreedySolver
import os
import json

for file in os.listdir("tests/"):
    if file.endswith(".in"):
        path = os.path.join("tests/", file)
        with open(path, "r") as f:
            print(path)
            input = json.load(f)
            greedySolver = GreedySolver(input)
            greedySolver()
            print(greedySolver.result)
            smartGreedySolver = SmartGreedySolver(input)
            smartGreedySolver()
            print(smartGreedySolver.result)
            dynamicSolver = DynamicSolver(input)
            dynamicSolver()
            print(dynamicSolver.result)

            def sum_results(result):
                return sum([i[0][0] for i in result]), sum([i[0][1] for i in result])

            print(sum_results(greedySolver.result), "|",
                  sum_results(smartGreedySolver.result), "|",
                  sum_results(dynamicSolver.result))

# for test in "tests/":
# wczytaj test
# gs = GreedySolver(wczytane_dane)
# gs()
# wynik_greedy = sum(gs.result, key=lambda x:x[0][0])
# smart...
# dynamic
# zapamietaj wyniki


# po petli: dla kazdego wyniku wyswietl: "sciezka testu", "wyniki 1, 2, 3" "N", "C"

