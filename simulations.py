import subprocess
import os

base_cmd = 'python3 main.py --algorithm all --parameters conf\\param'
base_cmd_sufix = '.conf tests\\12test_1000_500.in '

for i in [4,6,8,9,11,19]:
    #print (base_cmd+str(i)+base_cmd_sufix)
    os.system(base_cmd+str(i)+base_cmd_sufix)#"python3 main.py --algorithm all --parameters conf\\param2.conf tests\\01test_20_100.in ")
