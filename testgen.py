#!/bin/python
import random
import argparse
import numpy as np
import argparse
import json

parser = argparse.ArgumentParser(description="Generator testow na rzecz projektu z PSZT")
parser.add_argument('--filename', help="Sciezka pliku testowego", type=str, default="testowy.in")
parser.add_argument('licz_przedmiotow', help="Liczba przedmiotow ktore zostana wygenerowane", type=int)
parser.add_argument('pojemnosc_plecaka', help="Pojemnosc plecaka", type=int, default=50)
parser.add_argument('--srednia_wag', help="Srednia rozkladu normalnego dla wag", type=float, default=10, required=False)
parser.add_argument('--srednia_wartosci', help="Srednia rozkladu normalnego dla wartosci", type=float, default=10, required=False)
parser.add_argument('--wariancja_wag', help='Wariancja rozkladu normalnego dla wag', type=float, default=2, required=False)
parser.add_argument('--wariancja_wartosci', help='Wariancja rozkladu normalnego dla wartosci', type=float, default=2, required=False)
parser.add_argument('--nwd', help="Zadana najwieksza wspolna wielokrotnosc wag", type=int, default=1, required=False)
parser.add_argument('-v', help="Tryb verbose", action="store_true")

args = parser.parse_args()

file_path = args.filename
N = args.licz_przedmiotow
v = args.pojemnosc_plecaka
mu_w = args.srednia_wag
mu_p = args.srednia_wartosci
sigma_w = args.wariancja_wag
sigma_p = args.wariancja_wartosci

items_list = []
nwd = args.nwd
for x in range(0, int(N)):
    waga = max(int(np.random.normal(mu_w, sigma_w, 1)), 1)  # FIXME wagi i wartosci powinny moc miec inne rozklady.
    if nwd > 1:
        waga = max(nwd, int(waga / nwd) * nwd)
    wartosc = int(np.random.normal(mu_p, sigma_p, 1))

    items_list.append((wartosc, waga))

if args.v:
    print(items_list)

with open(file_path, "w") as myfile:
    json.dump({"capacity": v, "items_number": N, "items": items_list, "description": "prize/weight"}, myfile, indent=True)
