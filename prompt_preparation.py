import utils
import random
import string

random.seed(0)


def build_multiple_choice_semantic_relevance_prompt(data, _type):
    prompt_list = []
    for unit in data:
        question = unit['question']
        if _type == "unrelated":
            irrelevant_info_list = [unit["unrelated_info"]]
            option_list = [unit["memory_answer"], unit["unrelated_template"], "I'm not sure."]
        elif _type == "partially related":
            irrelevant_info_list = [unit["partially_related_info"]]
            option_list = [unit["memory_answer"], unit["partially_related_template"], "I'm not sure."]
        elif _type == "related":
            irrelevant_info_list = [unit["related_contriever_highest"]]
            option_list = [unit["memory_answer"], unit["related_template"], "I'm not sure."]
        else:
            raise ValueError("Unexpected type: " + _type)
        random.shuffle(irrelevant_info_list)
        random.shuffle(option_list)
        unit["option_list"] = option_list
        info_str = "\n".join([f"{i + 1}. {evidence}" for i, evidence in enumerate(irrelevant_info_list)])
        option_str = "\n".join([f"{letter}. {option.strip()}" for letter, option in zip(string.ascii_uppercase, option_list)])
        prompt_text = f"""According to the given information and your knowledge, choose the best choice from the following options.
Information:
{info_str}
Question:
{question}
Options:
{option_str}
Answer:"""
        prompt_list.append(prompt_text)
    return prompt_list, data


def build_multiple_choice_quantity_prompt(data, multi_irrelevant_info_flag, relevant_info_flag):
    prompt_list = []
    for unit in data:
        question = unit['question']
        if multi_irrelevant_info_flag:
            irrelevant_info_list = [unit['related_cc'], unit['related_ml'], unit['related_fa']]
        else:
            irrelevant_info_list = [unit['related_contriever_highest']]
        relevant_info_list = [unit['parametric_memory']] if relevant_info_flag else []
        info_list = irrelevant_info_list + relevant_info_list
        option_list = [unit["memory_answer"], unit["related_template"], "I'm not sure."]
        random.shuffle(info_list)
        random.shuffle(option_list)
        unit["info_list"] = info_list
        unit["option_list"] = option_list
        info_str = "\n".join([f"{i + 1}. {evidence}" for i, evidence in enumerate(info_list)])
        option_str = "\n".join([f"{letter}. {option.strip()}" for letter, option in zip(string.ascii_uppercase, option_list)])
        prompt_text = f"""According to the given information and your knowledge, choose the best choice from the following options.
Information:
{info_str}
Question:
{question}
Options:
{option_str}
Answer:"""
        prompt_list.append(prompt_text)
    return prompt_list, data


def build_format_prompt(data, format_type):
    prompt_list = []
    for unit in data:
        question = unit['question']
        related_template = unit['related_template']
        irrelevant_info_list = [unit['related_cc'], unit['related_ml'], unit['related_fa']]
        relevant_info_list = unit['parametric_memory']
        info_list = irrelevant_info_list + relevant_info_list
        option_list = [unit["memory_answer"], unit["related_template"], "I'm not sure."]
        random.shuffle(info_list)
        random.shuffle(option_list)
        unit["info_list"] = info_list
        unit["option_list"] = option_list
        info_str = "\n".join([f"{i + 1}. {evidence}" for i, evidence in enumerate(info_list)])
        option_str = "\n".join([f"{letter}. {option.strip()}" for letter, option in zip(string.ascii_uppercase, option_list)])
        if format_type == "boolean":
            prompt_text = f"""According to the given information and your knowledge, determine whether the statement is true or false.
Information:
{info_str}
Statement:
{related_template}
Is the statement true or false?"""
        elif format_type == "multiple choice":
            prompt_text = f"""According to the given information and your knowledge, choose the best choice from the following options.
Information:
{info_str}
Question:
{question}
Options:
{option_str}
Answer:"""
        elif format_type == "free form":
            prompt_text = f"""According to the given information and your knowledge, answer the question.
Information:
{info_str}
Question:
{question}
Answer:"""
        else:
            raise ValueError("Unexpected question format type: " + format_type)
        prompt_list.append(prompt_text)
    return prompt_list, data
