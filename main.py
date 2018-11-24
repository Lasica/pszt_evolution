#!/bin/python
import numpy as np
import argparse
import yaml
import time

timestr = time.strftime("%Y-%m-%d-%H-%M-%S")
algorithms = ["brute", "smartbrute", "evolution", "dynamic"]

outfile = "run{}.out".format(timestr)

parser = argparse.ArgumentParser(description="")
parser.add_argument('--test', help="Sciezka pliku testowego", type=str, default="testowy.csv")
parser.add_argument('--algorithm', help="Wybor algorytmu do rozwiazania", type=str, choices=algorithms)
args = parser.parse_args()
if __name__ == "__main__":
    print("Testing {} with {}, output file {}...".format(args.test, args.algorithm, outfile))

