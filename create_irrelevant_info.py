from dotenv import load_dotenv
import ast
import contriever
import utils
import json
from tqdm import tqdm
import prompt_preparation
from openai_request import prompt_chatgpt


def create_unrelated_info(dataset, output_path):
    prefix, path = utils.get_dataset_prefix_and_path(dataset)
    try:
        with open(f"{path}/{prefix}_prop.json", 'r') as json_file:
            data = json.load(json_file)
        with open(f"{path}/{prefix}_contriever_retrieved_docs_has_answer.json", 'r') as json_file:
            retrieved_docs = json.load(json_file)
    except:
        print("Files not found. Please download the files first.")
        return
    data_dict = utils.create_dict_id_to_data(data, False)
    _contriever = contriever.Contriever()
    print("Creating Unrelated Info...")
    for idx1, prop in enumerate(tqdm(data)):
        data_prop = data[prop]
        questions = [data_prop[i]['question'] for i in range(len(data_prop))]
        retrieved_docs_prop = retrieved_docs[prop]
        dumps = [retrieved_docs_prop[i]['text'] for i in range(len(retrieved_docs_prop))]
        similarity_scores = _contriever.compute_similarity(questions, dumps)
        for idx2, (query, scores_indices) in enumerate(similarity_scores):
            unit = data_prop[idx2]
            unit['unrelated_info'] = None
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
                unit['unrelated_info'] = irr_passage
                unit['unrelated_info_qid'] = irr_q_id
                break
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file)


def create_partially_related_info_p1(dataset):
    prefix, path = utils.get_dataset_prefix_and_path(dataset)
    ret_data = {}
    try:
        with open(f"{path}/{prefix}_prop.json", 'r') as json_file:
            data = json.load(json_file)
        with open(f"{path}/{prefix}_contriever_retrieved_docs.json", 'r') as json_file:
            retrieved_docs = json.load(json_file)
    except:
        print("Files not found. Please download the files first.")
        return
    _contriever = contriever.Contriever()
    print("Creating Partially Related Info p1...")
    for idx1, prop in enumerate(tqdm(data)):
        data_prop = data[prop]
        for idx2, unit in enumerate(data_prop):
            new_unit = {
                "partially_related_info_p1": None,
            }
            if prop not in ret_data:
                ret_data[prop] = [new_unit]
            else:
                ret_data[prop].append(new_unit)
            questions = [unit['question']]
            subj_aliases = ast.literal_eval(unit['s_aliases'])
            subj_aliases.append(unit['subj'])
            if subj_aliases[0] is None:
                continue
            obj_aliases = ast.literal_eval(unit['o_aliases'])
            obj_aliases.append(unit['obj'])
            unit_docs_hasnot_answer = []
            unit_docs = retrieved_docs[prop][idx2]
            for idx3, sent in enumerate(unit_docs['ctxs']):
                if sent['hasanswer']:
                    continue
                unit_docs_hasnot_answer.append(sent)
            dumps = [unit_docs_hasnot_answer[i]['text'] for i in range(len(unit_docs_hasnot_answer))]
            if len(dumps) == 0:
                continue
            similarity_scores = _contriever.compute_similarity(questions, dumps)
            _, scores_indices = similarity_scores[0]
            for score, idx3 in scores_indices:
                irr_tuple = unit_docs_hasnot_answer[idx3]
                irr_passage = irr_tuple['title'] + "--" + irr_tuple['text']
                if (not any(_subj in irr_passage for _subj in subj_aliases) or
                        any(obj in irr_tuple['title'] for obj in obj_aliases)):
                    continue
                new_unit["partially_related_info_p1"] = irr_passage
                break
    return ret_data


def create_partially_related_info_p2(dataset):
    prefix, path = utils.get_dataset_prefix_and_path(dataset)
    ret_data = {}
    try:
        with open(f"{path}/{prefix}_prop.json", 'r') as json_file:
            data = json.load(json_file)
        with open(f"{path}/{prefix}_contriever_retrieved_docs_has_answer.json", 'r') as json_file:
            retrieved_docs = json.load(json_file)
        with open(f"{path}/{prefix}_obj_wiki_intro.json", 'r') as json_file:
            obj_wiki_intro_dict = json.load(json_file)
    except:
        print("Files not found. Please download the files first.")
        return
    data_dict = utils.create_dict_id_to_data(data, False)
    _contriever = contriever.Contriever()
    print("Creating Partially Related Info p2...")
    for idx1, prop in enumerate(tqdm(data)):
        data_prop = data[prop]
        questions = [data_prop[i]['question'] for i in range(len(data_prop))]
        retrieved_docs_prop = retrieved_docs[prop]
        dumps = [retrieved_docs_prop[i]['text'] for i in range(len(retrieved_docs_prop))]
        similarity_scores = _contriever.compute_similarity(questions, dumps)
        for idx2, (query, scores_indices) in enumerate(similarity_scores):
            unit = data_prop[idx2]
            new_unit = {
                "partially_related_info_p2": None,
                "partially_related_info_qid": None,
            }
            if prop not in ret_data:
                ret_data[prop] = [new_unit]
            else:
                ret_data[prop].append(new_unit)
            q_id = unit['id']
            obj = unit['obj']
            for score, idx3 in scores_indices:
                irr_tuple = retrieved_docs_prop[idx3]
                irr_q_id = irr_tuple["q_id"]
                irr_s_aliases = ast.literal_eval(data_dict[irr_q_id]['s_aliases'])
                irr_s_aliases.append(data_dict[irr_q_id]['subj'])
                if irr_s_aliases[0] is None:
                    continue
                irr_obj_id = str(data_dict[irr_q_id]['obj_id'])
                if data_dict[irr_q_id]['question'] == data_dict[q_id]['question'] or \
                        data_dict[irr_q_id]['obj'] == obj:
                    continue
                obj_intro = obj_wiki_intro_dict[irr_obj_id]['obj_intro']
                if obj_intro is None or utils.count_words(obj_intro) < 10 or \
                        any(_alias in obj_intro for _alias in irr_s_aliases):
                    continue
                obj_intro = utils.first_100_words(obj_intro)
                new_unit['partially_related_info_p2'] = obj_intro
                new_unit['partially_related_info_qid'] = irr_q_id
                break
    return ret_data


def create_partially_related_info(dataset, output_path):
    prefix, path = utils.get_dataset_prefix_and_path(dataset)
    try:
        with open(f"{path}/{prefix}_prop.json", 'r') as json_file:
            data = json.load(json_file)
    except:
        print("Files not found. Please download the files first.")
        return
    partially_related_info_p1 = create_partially_related_info_p1(dataset)
    partially_related_info_p2 = create_partially_related_info_p2(dataset)
    for idx1, prop in enumerate(data):
        data_prop = data[prop]
        for idx2, unit in enumerate(data_prop):
            unit["partially_related_info"] = None
            unit["partially_related_info_qid"] = None
            p1_unit = partially_related_info_p1[prop][idx2]
            p2_unit = partially_related_info_p2[prop][idx2]
            if p1_unit["partially_related_info_p1"] is None or p2_unit["partially_related_info_p2"] is None:
                continue
            unit["partially_related_info"] = p1_unit["partially_related_info_p1"] + '\n' + p2_unit["partially_related_info_p2"]
            unit["partially_related_info_qid"] = p2_unit["partially_related_info_qid"]
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file)


def create_related_info(dataset, output_path):
    prefix, path = utils.get_dataset_prefix_and_path(dataset)
    try:
        with open(f"{path}/{prefix}_partially_related.json", 'r') as json_file:
            data = json.load(json_file)
    except:
        print("Files not found. Please download the files first.")
        return
    data_lines = []
    data_dict = utils.create_dict_id_to_data(data, False)
    for idx1, prop in enumerate(data):
        data_prop = data[prop]
        for idx2, unit in enumerate(data_prop):
            data_lines.append(unit)
    prompt_list = prompt_preparation.build_related_info_prompt(data_lines, data_dict, dataset)
    total_price = 0
    for idx, prompt in enumerate(tqdm(prompt_list[:10])):
        if prompt == "":
            with open(output_path, 'a+', encoding='utf-8') as f:
                assistant_output = str(idx)
                f.write(assistant_output + '\n')
            continue
        results, _, price = prompt_chatgpt("You are a helpful assistant.", index=idx, save_path=output_path,
                                           user_input=prompt, model_name="gpt-4-1106-preview", temperature=0)
        total_price += price
    print("Total Price: ", total_price)


def create_irrelevant_info(_type, dataset, output_path):
    if _type == "unrelated":
        create_unrelated_info(dataset, output_path)
    elif _type == "partially_related":
        create_partially_related_info(dataset, output_path)
    elif _type == "related":
        create_related_info(dataset, output_path)
    else:
        raise ValueError("Unexpected Irrelevant Infomation Type: " + _type)


if __name__ == "__main__":
    load_dotenv()
    create_irrelevant_info("related", "EQ", "raw_data_and_contriever_docs/Irrelevant_EntityQuestions/EQ_test_related.txt")
