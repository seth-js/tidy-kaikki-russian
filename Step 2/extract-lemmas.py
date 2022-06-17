import json
import re

print("Loading Russian Wiktionary data...")

with open("ru-wikiextract.json", encoding="utf-8") as f:
    dict = json.load(f)

print("Data loaded...")

lemmas = {}

degree_words = []
possible_misspellings = []

for entry in dict:
    word = entry["word"]

    categories = ""

    try:
        categories = entry["categories"]
    except KeyError:
        msg = "this entry has no categories"

    if categories != "":
        if "Russian non-lemma forms" in categories:
            senses = ""

            try:
                senses = entry["senses"]
            except KeyError:
                msg = "this entry has no senses"

            if senses != "":
                for sense in senses:
                    raw_glosses = []

                    try:
                        raw_glosses = sense["raw_glosses"]
                    except KeyError:
                        msg = "this entry has no glosses"

                    for gloss in raw_glosses:
                        if re.search(r"^superlative", gloss):
                            form_of = re.sub(r".+?of |\s\(.+|[́]", "", gloss)
                            degree_words.append(
                                {
                                    "word": word,
                                    "form_of": form_of,
                                    "degree": "superlative",
                                }
                            )
                        elif re.search(r"^comparative", gloss):
                            form_of = re.sub(r".+?of |\s\(.+|[́]", "", gloss)
                            degree_words.append(
                                {
                                    "word": word,
                                    "form_of": form_of,
                                    "degree": "comparative",
                                }
                            )

        if "Russian lemmas" in categories:
            if word not in lemmas:
                lemmas[word] = [entry]
            else:
                lemmas[word].append(entry)

            if "ё" in word and word not in possible_misspellings:
                possible_misspellings.append(word)

    senses = ""

    try:
        senses = entry["senses"]
    except KeyError:
        msg = "this entry has no senses"

    if senses != "":

        for sense in senses:
            categories = ""

            try:
                categories = sense["categories"]
            except KeyError:
                msg = "this sense has no categories"

            if categories != "":
                if "Russian lemmas" in categories:
                    if word not in lemmas:
                        lemmas[word] = [entry]
                    else:
                        lemmas[word].append(entry)

                    if "ё" in word and word not in possible_misspellings:
                        possible_misspellings.append(word)
                if "Russian non-lemma forms" in categories:
                    senses = ""

                    try:
                        senses = entry["senses"]
                    except KeyError:
                        msg = "this entry has no senses"

                    if senses != "":
                        for sense in senses:
                            raw_glosses = []

                            try:
                                raw_glosses = sense["raw_glosses"]
                            except KeyError:
                                msg = "this entry has no glosses"

                            for gloss in raw_glosses:
                                if re.search(r"^superlative", gloss):
                                    form_of = re.sub(r".+?of |\s\(.+|[́]", "", gloss)
                                    degree_words.append(
                                        {
                                            "word": word,
                                            "form_of": form_of,
                                            "degree": "superlative",
                                        }
                                    )
                                elif re.search(r"^comparative", gloss):
                                    form_of = re.sub(r".+?of |\s\(.+|[́]", "", gloss)
                                    degree_words.append(
                                        {
                                            "word": word,
                                            "form_of": form_of,
                                            "degree": "comparative",
                                        }
                                    )

for entry in degree_words:
    word = entry["word"]
    form_of = entry["form_of"]
    degree = entry["degree"]

    try:
        if lemmas[form_of]:
            for res in lemmas[form_of]:
                res["forms"].append({"form": word, "tags": [degree]})

    except KeyError:
        msg = "the form it points to doesn't have a lemma entry"


for word in possible_misspellings:
    misspelling = re.sub(r"ё", "е", word)

    for res in lemmas[word]:
        res["forms"].append({"form": misspelling, "tags": ["alternate-form"]})


result = []

for entry in lemmas:
    info = lemmas[entry]

    result.append({"word": entry, "info": info})


with open("ru-lemmas.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False)
