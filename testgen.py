#!/bin/python
import random
import argparse
import numpy as np
import argparse
import yaml

parser = argparse.ArgumentParser(description="Generator testow na rzecz projektu z PSZT")
parser.add_argument('--filename', help="Sciezka pliku testowego", type=str, default="testowy.in")
parser.add_argument('licz_przedmiotow', help="Liczba przedmiotow ktore zostana wygenerowane", type=int)
parser.add_argument('pojemnosc_plecaka', help="Pojemnosc plecaka", type=int, default=50)
parser.add_argument('--srednia', help="Srednia rozkladu normalnego", type=float, default=10, required=False)
parser.add_argument('--wariancja', help='Wariancja rozkladu normalnego', type=float, default=2, required=False)
parser.add_argument('--nwd', help="Zadana najwieksza wspolna wielokrotnosc wag", type=int, default=1, required=False)



args = parser.parse_args()

file_path = args.filename
N = args.licz_przedmiotow
v = args.pojemnosc_plecaka
mu = args.srednia
sigma = args.wariancja

items_list = []
nwd = args.nwd
for x in range(0, int(N)):
    waga    = int(np.random.normal(mu, sigma, 1))
    if(nwd > 1):
        waga = min(nwd, int(waga/nwd)*nwd)
    wartosc = int(np.random.normal(mu, sigma, 1))
    
    items_list.append((waga, wartosc))

print(items_list)

with open(file_path, "w") as myfile:
    yaml.dump({"volume": v, "items_number": N, "items": items_list, "description": "weight/value"}, stream=myfile)


