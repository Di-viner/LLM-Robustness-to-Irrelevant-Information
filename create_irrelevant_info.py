import ast
import contriever
import utils
import json
from tqdm import tqdm
from dotenv import load_dotenv


def create_irrelevant_info(_type, dataset, output_path):
    if _type == "unrelated":
        create_unrelated_info(dataset, output_path)
    elif _type == "partially_related":
        # TODO
        pass
    elif _type == "related":
        # TODO
        pass
    else:
        raise ValueError("Unexpected Irrelevant Infomation Type: " + _type)

def create_unrelated_info(dataset, output_path):
    prefix, path = utils.load_path(dataset)
    try:
        with open(f"{path}/{prefix}_prop.json", 'r') as json_file:
            data = json.load(json_file)
        with open(f"{path}/{prefix}_contriever_retrieved_docs_has_answer.json", 'r') as json_file:
            retrieved_docs = json.load(json_file)
    except:
        print("Files not found. Please download the files first.")
        return
    data_dict = utils.create_dict_id_to_data(data, False)
    contriever_ = contriever.Contriever()
    for idx1, prop in enumerate(tqdm(data)):
        data_prop = data[prop]
        questions = [data_prop[i]['question'] for i in range(len(data_prop))]
        retrieved_docs_prop = retrieved_docs[prop]
        dumps = [retrieved_docs_prop[i]['text'] for i in range(len(retrieved_docs_prop))]

        similarity_scores = contriever_.compute_similarity(questions, dumps)

        for idx2, (query, scores_indices) in enumerate(similarity_scores):
            unit = data_prop[idx2]
            unit['unrelated'] = None
            q_id = unit['id']
            obj = unit['obj']
            s_aliases = ast.literal_eval(unit['s_aliases'])
            s_aliases.append(unit['subj'])
            if s_aliases[0] is None:
                continue

            for score, idx3 in scores_indices:
                irr_tuple = retrieved_docs_prop[idx3]
                irr_passage = irr_tuple['title'] + "--" + irr_tuple['text']
                irr_q_id = irr_tuple["q_id"]

                if data_dict[irr_q_id]['question'] == data_dict[q_id]['question'] or \
                        data_dict[irr_q_id]['obj'] == obj or \
                        data_dict[irr_q_id]['subj'] is None:
                    continue

                irr_s_aliases = ast.literal_eval(data_dict[irr_q_id]['s_aliases'])
                irr_s_aliases.append(data_dict[irr_q_id]['subj'])

                if (not any(_subj in irr_passage for _subj in irr_s_aliases)) or \
                        any(subj in irr_passage for subj in s_aliases):
                    continue
                unit['unrelated'] = irr_passage
                unit['unrelated_qid'] = irr_q_id
                break
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file)


if __name__ == "__main__":
    load_dotenv()
    create_irrelevant_info("unrelated", "EQ", "data/Irrelevant_EntityQuestions/Irrelevant_EQ_unrelated.json")
    print("Unrelated")
