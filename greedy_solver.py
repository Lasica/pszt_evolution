#open file, read list of items, sort them and put in backpack
import yaml

file_path = "testowy.csv"
with open(file_path) as f:
	yamlcha    = yaml.load(f)
	item_dict  = yamlcha["items"]
	max_weight = yamlcha["volume"]
	item_num   = yamlcha["items_number"] 

item_dict = [(price,weight) for (weight,price) in item_dict]
item_dict.sort()

current_prize = 0
plecak = []

for (price,weight) in item_dict:
	while (cur_weight+item_weight)<max_weight:
		current_prize  += price
		current_weight += weigt
		plecak.append(price,weight)

print(plecak)
return plecak