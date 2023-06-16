# import json
# f = open("confusables.txt", "r", encoding="utf-8")
# r = f.readlines()

# # Opening JSON file
# with open('normalized.json') as json_file:
#     dictionary = json.load(json_file)

# for l in r:
#     if '←' in l:
#         print(l.rstrip()[-1])   

# with open("out.json", "w") as outfile:
#     json.dump(dictionary, outfile)
import json

with open('normalized.json', 'r', encoding='utf-8') as json_file:
    dictionary = json.load(json_file)
[print(x) for x in dictionary.keys()]

while True:
    inp = input()
    with open('normalized.json', 'r', encoding='utf-8') as json_file:
        dictionary = json.load(json_file)

    a = inp.replace('\t', '').replace(' ', '')

    print(a)
    dictionary[a[0]] = [x for x in a]
    print(dictionary)
    with open("normalized.json", "w", encoding='utf-8') as outfile:
        json.dump(dictionary, outfile)
