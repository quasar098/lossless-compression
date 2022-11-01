from copy import deepcopy
from itertools import combinations
from os import listdir


symbols = "☀☂☃☄★☆☇☈☉☊☋☌☍☎☏"
cdict = {}
possible_texts = listdir("texts")
for index, possible_text in enumerate(possible_texts):
    print(f"{possible_text[:-4]} ({index})")


file_to_read = int(input("Choose a file to read > "))


with open(f"texts\\{possible_texts[file_to_read]}", 'r') as file:
    text = file.read().lower().replace("\n", '')


def sub(to_replace: str):
    for symbol in cdict:
        if cdict[symbol] is None:
            continue
        to_replace = to_replace.replace(cdict[symbol], symbol)
    if len([1 for compre in cdict if cdict[compre] is not None and cdict[compre] in to_replace]):
        return sub(to_replace)
    return to_replace


def compression_ratio():
    compressed = sub(deepcopy(text))
    compressed_size = len(compressed)
    compressed_size += len(''.join([wasd for wasd in cdict if cdict[wasd] is not None]))
    compressed_size += len(''.join([cdict[wasd] for wasd in cdict if cdict[wasd] is not None]))

    return round((1-compressed_size/len(text))*10000)/100


def apply(symbol: str):
    global text
    temp_text = text
    for dict_key in cdict:
        if dict_key == symbol:
            break
        if cdict[dict_key] is not None:
            temp_text = temp_text.replace(cdict[dict_key], dict_key)

    prev_ratio = compression_ratio()
    combos = [temp_text[x:y] for x, y in combinations(range(len(temp_text) + 1), r=2)]
    scores = {}

    for dict_value in combos:
        cdict[symbol] = dict_value
        scores[dict_value] = compression_ratio()

    sorted_scores = [k for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True) if len(k) < 20]
    best_score = sorted_scores[0]

    cdict[symbol] = best_score
    if compression_ratio() < prev_ratio:
        cdict[symbol] = None
        out = f"{compression_ratio()}\t{symbol}\tCAN'T OPTIMIZE"
    else:
        out = f"{compression_ratio()}\t{symbol}\t{best_score}"

    return out


def run_pass():
    print("Running pass")
    for symbol in symbols:
        apply(symbol)
    print("Done pass")


for i in range(4):
    run_pass()

formatted_result = "\n" + "\n".join([cdict[pair] for pair in cdict if cdict[pair] is not None])

print(formatted_result)
