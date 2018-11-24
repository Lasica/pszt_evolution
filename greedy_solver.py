#open file, read list of items, sort them and put in backpack
import yaml

file_path = "tests\\test_prosty.in"
with open(file_path) as f:
	yamlcha    = yaml.load(f)
	item_dict  = yamlcha["items"]
	max_weight = yamlcha["volume"]
	item_num   = yamlcha["items_number"] 

item_dict = [(price,weight, i) for i, (weight,price) in enumerate(item_dict)]
item_dict.sort(reverse=True)

print(item_dict)
current_prize = 0
current_weight = 0
plecak = []

for (weight, price, num) in item_dict:
	print(current_weight, current_prize, price, weight)
	if (current_weight + weight) <= max_weight:
		current_prize  += price
		current_weight += weight
		plecak.append((price, weight, num))

print(plecak, current_prize, current_weight)

