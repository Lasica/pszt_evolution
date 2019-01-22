#!/bin/python
import argparse
import json
import time
from solvers.DynamicSolver import DynamicSolver
from solvers.GreedySolver import GreedySolver
from solvers.SmartGreedySolver import SmartGreedySolver
from solvers.GeneticSolver import GeneticSolver
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
import os



timestr = time.strftime("%Y-%m-%d-%H-%M-%S")
algorithms = ["greedy", "smartgreedy", "dynamic", "evolution", "all"]

outfile = "run{}.out".format(timestr)

parser = argparse.ArgumentParser(description="")
parser.add_argument('test', help="Sciezka pliku testowego", type=str)
parser.add_argument('--algorithm', help="Wybor algorytmu do rozwiazania", type=str, choices=algorithms, default='all')
parser.add_argument('--parameters', help="Parametry do przekazania dla algorytmu", type=str, default=None)
args = parser.parse_args()


def load(path):
    with open(path, 'r') as file:
        return json.load(file)

def create_solver(algorithm, data, parameters):
    print("Creating {} solver...".format(algorithm))
    if algorithm == algorithms[0]:  # greedy
        return GreedySolver(data)

    elif algorithm == algorithms[1]:  # smart greedy
        return SmartGreedySolver(data)

    elif algorithm == algorithms[2]:  # dynamic
        return DynamicSolver(data)

    elif algorithm == algorithms[3]:  # evolution
        return GeneticSolver(data, parameters)

    elif algorithm != 'all':  # all of them - comparison
        raise Exception("Unknown algorithm type")  # nie powinno sie wydarzyc, argparse sprawdza skladnie

def verbose_solving(solver):
    print("Solving...")
    solver()
    print("Solved in {} with result: <score> {}".format(solver.get_solving_time(), solver.get_score()))
    print("[" + str(solver.result[:10]) + ("...]" if len(solver.result)>10 else "]"))

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
        'record': 1,
        'selection': "roulette",
        'cross_points': 2,
        'mutation': 0.8,
        'mi': 20,
        'lambda': 10,
        'translator': 'permutation',
        'max_iterations': 500,
<<<<<<< HEAD
        'verbose': True#False,

=======
>>>>>>> 037feb55e805d0247e1e6b09fc04bfef880f17be
    }
    if args.parameters:
        parameters = load(args.parameters)
    else:
        try:
            parameters = load("default_parameters.conf")
        except:
            print("Missing default config file or invalid, replacing with new one.")
            with open("default_parameters.conf", "w") as f:
                json.dump(default_config, f, indent=True)
            parameters = default_config

    if args.algorithm == 'all':
        if parameters['record'] <= 0:
            raise Exception("When comparing all methods record has to be enabled")
        plt.style.use('dark_background')
        greedy      = create_solver('greedy', test_data, parameters)
        sgreedy     = create_solver('smartgreedy', test_data, parameters)
        dynamic     = create_solver('dynamic', test_data, parameters)
        evolution   = create_solver("evolution", test_data, parameters)
        verbose_solving(greedy)
        verbose_solving(sgreedy)
        verbose_solving(dynamic)
        # import numpy as np
        # np.seterr(all='raise')
        verbose_solving(evolution)
        figure = plt.figure(figsize=(11,7))
        ax = figure.subplots()
        xdata = [-10, parameters['max_iterations']+1]
        #ydata = [greedy.get_score()[0] for i in range(2)]
        #ax.annotate('greedy', (xdata[1]-2, ydata[1]))
        #ax.add_line(Line2D(xdata, ydata, linewidth=0.5, linestyle='dashed', color='red'))
        #ydata = [sgreedy.get_score()[0] for i in range(2)]
        #ax.annotate('smart', (xdata[1]-2, ydata[1]))
        #ax.add_line(Line2D(xdata, ydata, linewidth=0.5, linestyle='dashed', color='blue'))
        #ydata = [dynamic.get_score()[0] for i in range(2)]
        #ax.annotate('optimal', (xdata[1]-2, ydata[1]))
        #ax.add_line(Line2D(xdata, ydata, linewidth=0.5, linestyle='dashed', color='yellow'))


        # ax.annotate('evolution', (xdata[1] - 2, evolution.get_score()[0]))


        pool_scores = [map(lambda x:x[0], row) for row in evolution.history['pool']]
        child_scores = [map(lambda x:x[0], row) for row in evolution.history['children']]

        xdata = [i for i in range(0, parameters['max_iterations'], parameters['record'])]
        pop_count = parameters['mi']
        child_count = parameters['lambda']

        for ydata in zip(*pool_scores):
           ax.scatter(xdata, ydata, marker='.', s=2, color='orange')


        for ydata in zip(*child_scores):
            ax.scatter(xdata, ydata, marker='.', s=2, color='green')#niebieskie
        ax.set_xlim(left=-5, right=xdata[-1])
        ax.set_title("μ={}, λ={}, Mut={}, CP={}, selekcja={}, {}, translator={}".format(
                        parameters["mi"],
                        parameters["lambda"],
                        parameters["mutation"],
                        parameters["cross_points"],
                        parameters["selection"],
                        0.5, # todo: wstawic presje selekcyjna
                        parameters["translator"],
                        args.test)
                     )
        # import pdb; pdb.set_trace()
        ax.set_xlabel("Iteracja algorytmu genetycznego")
        ax.set_ylabel("Wartość upakowania plecaka")
        figure.tight_layout()
        i = 0
        while os.path.exists("symulacja{:03d}.png".format(i)):
            i += 1
        filename = "symulacja{:03d}.png".format(i)

        figure.savefig(filename)
    else:
        solver = create_solver(args.algorithm, test_data, parameters)
        verbose_solving(solver)
