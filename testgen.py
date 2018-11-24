#!/bin/python
import random
import argparse
import numpy as np
import argparse
import yaml

parser = argparse.ArgumentParser(description="Generator testów na rzecz projektów z PSZT")
parser.add_argument('--filename', help="Ścieżka pliku testowego", type=str, default="testowy.csv")
parser.add_argument('licz_przedmiotow', help="Liczba przedmiotów które wygenerujemy", type=int)
parser.add_argument('pojemnosc_plecaka', help="Pojemność naszego plecaka", type=int, default=50)
parser.add_argument('--srednia', help="Średnia rozkładu normalnego", type=float, default=10, required=False)
parser.add_argument('--wariancja', help='Wariancja rozkładu normalnego', type=float, default=2, required=False)



args = parser.parse_args()

file_path = args.filename
N = args.licz_przedmiotow
v = args.pojemnosc_plecaka
mu = args.srednia
sigma = args.wariancja

items_list = []

for x in range(0, int(N)):
    waga    = int(np.random.normal(mu, sigma, 1))
    wartosc = int(np.random.normal(mu, sigma, 1))

    items_list.append((waga, wartosc))

print(items_list)

with open(file_path, "w") as myfile:
    yaml.dump({"volume":v, "items_number":N, "items":items_list}, stream=myfile)


