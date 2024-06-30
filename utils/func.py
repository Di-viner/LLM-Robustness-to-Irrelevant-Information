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


def build_claim(dataset, relation, subj, obj):
    if dataset == "PQA":
        return build_claim_PQA(relation, subj, obj)
    elif dataset == "EQ":
        return build_claim_EQ(relation, subj, obj)
    else:
        raise ValueError("Unexpected Dataset: " + dataset)

def build_claim_PQA(relation, subj, obj):
    if relation == "occupation":
        return subj + "'s occupation is " + obj + '.'
    elif relation == "place of birth":
        return subj + " was born in " + obj + '.'
    elif relation == "genre":
        return "The genre of " + subj + " is " + obj + '.'
    elif relation == "father":
        return obj + " is the father of " + subj + '.'
    elif relation == "country":
        return subj + " is in " + obj + '.'
    elif relation == "producer":
        return obj + ' is the producer of ' + subj + '.'
    elif relation == "director":
        return obj + ' is the director of ' + subj + '.'
    elif relation == "capital of":
        return subj + ' is the capital of ' + obj + '.'
    elif relation == "screenwriter":
        return obj + ' is the screenwriter for ' + subj + '.'
    elif relation == "composer":
        return obj + ' was the composer of ' + subj + '.'
    elif relation == "color":
        return "The color of " + subj + " is " + obj + '.'
    elif relation == "religion":
        return obj + " is the religion of " + subj + '.'
    elif relation == "sport":
        return subj + " plays " + obj + '.'
    elif relation == "author":
        return obj + " is the author of " + subj + '.'
    elif relation == "mother":
        return obj + " is the mother of " + subj + '.'
    elif relation == "capital":
        return obj + " is the capital of " + subj + '.'
    else:
        raise ValueError("Wrong Relation " + relation)


def build_claim_EQ(relation, subj, obj):
    if relation == 'headquarter':
        return "The headquarter of " + subj + " is located in " + obj + '.'
    elif relation == "founder":
        return subj + " was founded by " + obj + '.'
    elif relation == "deathplace":
        return subj + " died in " + obj + '.'
    elif relation == "performer":
        return subj + " was performed by " + obj + '.'
    elif relation == "located in":
        return subj + " is located in " + obj + '.'
    elif relation == "location of discovery":
        return subj + " was founded in " + obj + '.'
    elif relation == "recordlabel":
        return subj + " is represented by the music label " + obj + '.'
    elif relation == "country":
        return subj + " was created in " + obj + '.'
    elif relation == "spouse":
        return subj + " is married to " + obj + '.'
    elif relation == "creator":
        return subj + " was created by " + obj + '.'
    elif relation == "location":
        return subj + " is located in " + obj + '.'
    elif relation == "educated at":
        return subj + " was educated at " + obj + '.'
    elif relation == "notable work":
        return subj + " is famous for " + obj + '.'
    elif relation == "language":
        return subj + " was written in " + obj + '.'
    elif relation == "child":
        return subj + "'s child is " + obj + '.'
    elif relation == "manufacturer":
        return subj + " is produced by " + obj + '.'
    elif relation == "owned by":
        return subj + " is owned by " + obj + '.'
    else:
        raise ValueError("Wrong Relation " + relation)

