#!/bin/python
import numpy as np
import argparse
import json
import time
from solvers.DynamicSolver import DynamicSolver
from solvers.GreedySolver import GreedySolver
from solvers.SmartGreedySolver import SmartGreedySolver
from solvers.GeneticSolver import GeneticSolver


timestr = time.strftime("%Y-%m-%d-%H-%M-%S")
algorithms = ["greedy", "smartgreedy", "dynamic", "evolution"]

outfile = "run{}.out".format(timestr)

parser = argparse.ArgumentParser(description="")
parser.add_argument('test', help="Sciezka pliku testowego", type=str)
parser.add_argument('--algorithm', help="Wybor algorytmu do rozwiazania", type=str, choices=algorithms, required=True)
parser.add_argument('--parameters', help="Parametry do przekazania dla algorytmu", type=str, default=None)
args = parser.parse_args()


def load(path):
    with open(path, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    print("Testing {} with {}, output file {}...".format(args.test, args.algorithm, outfile))

    test_data = load(args.test)
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
    default_config = {
        'record': True,
        'selection': "roulette",
        'cross_points': 2,
        'mutation': 0.2,
        'mi': 20,
        'lambda': 10,
        'transaltor': 'permutation',
    }
    parameters = default_config
    if args.parameters:
        parameters = load(args.parameters)

    print("Selecting chosen solver...")
    solver = None
    if args.algorithm == algorithms[0]:  # greedy
        solver = GreedySolver(test_data)
    elif args.algorithm == algorithms[1]:  # smart greedy
        solver = SmartGreedySolver(test_data)
    elif args.algorithm == algorithms[2]:  # dynamic
        solver = DynamicSolver(test_data)
    elif args.algorithm == algorithms[3]:  # evolution
        solver = GeneticSolver(test_data, parameters)
    else:
        raise Exception("Unknown algorithm type")  # nie powinno sie wydarzyc, argparse sprawdza skladnie

    print("Solving...")
    solver()
    print("Solved in {} with result {}:".format(solver.get_solving_time(), -solver.check_answer(0)))
    print(solver.result)
