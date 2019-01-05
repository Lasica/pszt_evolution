#!/bin/bash
BP=1000
N=5000
echo Generowanie $1 testow... $#
for i in $(seq 1 $1); do
	echo Generating $i test
	python3 ../testgen.py $N $BP -s 50 -S 1000 -w 12 -W 100 -n 2;
	mv testowy.in test_"$N"_"$BP"_"$i".in;
done
