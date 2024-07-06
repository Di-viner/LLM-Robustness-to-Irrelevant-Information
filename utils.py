import json
import re
import os


def load_line_json_data(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.read().strip().split('\n'):
            unit = json.loads(line)
            data.append(unit)
    return data


def save_file(data, path):
    with open(path, 'w', encoding='utf-8') as w:
        for unit in data:
            output = json.dumps(unit)
            w.write(output + "\n")
        w.close()


def get_dataset_prefix_and_path(file_name):
    if file_name.lower() in ["pqa", "popqa"]:
        prefix = "Irrelevant_PQA"
        path = "data/Irrelevant_PopQA"
    elif file_name.lower() in ["eq", "entityquestions"]:
        prefix = "Irrelevant_EQ"
        path = "data/Irrelevant_EntityQuestions"
    else:
        raise ValueError("Unexpected Dataset: " + file_name)
    return prefix, path


def create_dict_id_to_data(data, line_flag):
    dict = {}
    if line_flag:
        for unit in data:
            dict[unit['id']] = unit
    else:
        for prop in data:
            for unit in data[prop]:
                dict[unit['id']] = unit
    return dict


def count_words(text):
    try:
        words = re.findall(r'\b\w+\b', text)
    except:
        return 0
    return len(words)


def first_100_words(text):
    words = text.split()
    return ' '.join(words[:100])


def build_claim(dataset, relation, subj, obj, induce=False):
    if dataset == "PQA":
        return build_claim_PQA(relation, subj, obj, induce)
    elif dataset == "EQ":
        return build_claim_EQ(relation, subj, obj, induce)
    else:
        raise ValueError("Unexpected Dataset: " + dataset)


def build_claim_PQA(relation, subj, obj, induce=False):
    if relation == "occupation":
        return subj + "'s occupation is" + ("/is not " if induce else " ") + obj + ("" if induce else ".")
    elif relation == "place of birth":
        return subj + " was" + ("/was not " if induce else " ") + "born in " + obj + ("" if induce else ".")
    elif relation == "genre":
        return "The genre of " + subj + " is" + ("/is not " if induce else " ") + obj + ("" if induce else ".")
    elif relation == "father":
        return obj + " is" + ("/is not " if induce else " ") + "the father of " + subj + ("" if induce else ".")
    elif relation == "country":
        return subj + " is" + ("/is not " if induce else " ") + "in " + obj + ("" if induce else ".")
    elif relation == "producer":
        return obj + " is" + ("/is not " if induce else " ") + "the producer of " + subj + ("" if induce else ".")
    elif relation == "director":
        return obj + " is" + ("/is not " if induce else " ") + "the director of " + subj + ("" if induce else ".")
    elif relation == "capital of":
        return subj + " is" + ("/is not " if induce else " ") + "the capital of " + obj + ("" if induce else ".")
    elif relation == "screenwriter":
        return obj + " is" + ("/is not " if induce else " ") + "the screenwriter for " + subj + ("" if induce else ".")
    elif relation == "composer":
        return obj + " was" + ("/was not " if induce else " ") + "the composer of " + subj + ("" if induce else ".")
    elif relation == "color":
        return "The color of " + subj + " is" + ("/is not " if induce else " ") + obj + ("" if induce else ".")
    elif relation == "religion":
        return obj + " is" + ("/is not " if induce else " ") + "the religion of " + subj + ("" if induce else ".")
    elif relation == "sport":
        return subj + " plays" + ("/doesn't play " if induce else " ") + obj + ("" if induce else ".")
    elif relation == "author":
        return obj + " is" + ("/is not " if induce else " ") + "the author of " + subj + ("" if induce else ".")
    elif relation == "mother":
        return obj + " is" + ("/is not " if induce else " ") + "the mother of " + subj + ("" if induce else ".")
    elif relation == "capital":
        return obj + " is" + ("/is not " if induce else " ") + "the capital of " + subj + ("" if induce else ".")
    else:
        raise ValueError("Wrong Relation " + relation)


def build_claim_EQ(relation, subj, obj, induce=False):
    if relation == "headquarters location":
        return "The headquarter of " + subj + " is" + ("/is not " if induce else " ") + "located in " + obj + ("" if induce else ".")
    elif relation == "founded by":
        return subj + " was" + ("/was not " if induce else " ") + "founded by " + obj + ("" if induce else ".")
    elif relation == "place of death":
        return subj + " died" + ("/doesn't die " if induce else " ") + "in " + obj + ("" if induce else ".")
    elif relation == "performer":
        return subj + " was" + ("/was not " if induce else " ") + "performed by " + obj + ("" if induce else ".")
    elif relation == "location_P131":
        return subj + " is" + ("/is not " if induce else " ") + "located in " + obj + ("" if induce else ".")
    elif relation == "location of formation":
        return subj + " was" + ("/was not " if induce else " ") + "founded in " + obj + ("" if induce else ".")
    elif relation == "record label":
        return subj + " is" + ("/is not " if induce else " ") + "represented by the music label " + obj + ("" if induce else ".")
    elif relation == "country":
        return subj + " was" + ("/was not " if induce else " ") + "created in " + obj + ("" if induce else ".")
    elif relation == "spouse":
        return subj + " is" + ("/is not " if induce else " ") + "married to " + obj + ("" if induce else ".")
    elif relation == "creator":
        return subj + " was" + ("/was not " if induce else " ") + "created by " + obj + ("" if induce else ".")
    elif relation == "location_P276":
        return subj + " is" + ("/is not " if induce else " ") + "located in " + obj + ("" if induce else ".")
    elif relation == "educated at":
        return subj + " was" + ("/was not " if induce else " ") + "educated at " + obj + ("" if induce else ".")
    elif relation == "notable work":
        return subj + " is" + ("/is not " if induce else " ") + "famous for " + obj + ("" if induce else ".")
    elif relation == "language":
        return subj + " was" + ("/was not " if induce else " ") + "written in " + obj + ("" if induce else ".")
    elif relation == "child":
        return subj + "'s child is" + ("/is not " if induce else " ") + obj + ("" if induce else ".")
    elif relation == "manufacturer":
        return subj + " is" + ("/is not " if induce else " ") + "produced by " + obj + ("" if induce else ".")
    elif relation == "owned by":
        return subj + " is" + ("/is not " if induce else " ") + "owned by " + obj + ("" if induce else ".")
    else:
        raise ValueError("Wrong Relation " + relation)
