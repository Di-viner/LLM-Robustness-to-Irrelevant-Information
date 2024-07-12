import utils
import re


uncertain_phrases = ["not specif", "not mention", "not possible",
                       "no indication", "no specif", "no mention", "no information", "no data",
                       "do not have", "does not", "I'm sorry", "I'm not sure", "neither",
                       "cannot determine", "cannot provide", "cannot be determined", "is not provided", "none of"]


def evaluate_multichoice(data, input_file, irr_template, cot_flag=False):
    with open(input_file, 'r') as input_file:
        lines = input_file.readlines()
    output_mappings = {}
    for output in lines:
        if not cot_flag:
            match = re.search(r'(\d+)\s+.*?(?:\b[Oo]ption\b\s+([A-C])\b|\b([A-C])\b\.|\(([A-C])\)|\b([A-C])\b)', output)
        else:
            match = re.search(
                r'(\d+)\s+.*?(?:(?:answer|best\schoice)\s(?:would be|is)\s*:?\s*(?:[Oo]ption\s)?\(?([A-C])\)?(?!\w)|\(?([A-C])\)?\s(?:would be|is)\s(?:the\s)?(?:correct|best)\s(?:answer|choice)?)',
                output)
        if match:
            index = int(match.group(1))
            if not cot_flag:
                option_letter = match.group(2) or match.group(3) or match.group(4) or match.group(5)
            else:
                option_letter = match.group(2) or match.group(3)
            output_mappings[index] = option_letter
        else:
            match = re.match(r'(\d+)\s+(.*)', output)
            if match:
                index = int(match.group(1))
                output_mappings[index] = match.group(2).strip()
    total_count, consist_count, changed_count, uncertain_count, unknown_count = 0, 0, 0, 0, 0
    for i, d in enumerate(data):
        model_option_info = output_mappings.get(i)
        if model_option_info is None:
            continue
        if len(model_option_info) == 1 and model_option_info in "ABC":
            model_option_index = ord(model_option_info) - ord('A')
            model_answer = d["option_list"][model_option_index]
        else:
            model_answer = model_option_info if "option_list" in d else None
        total_count += 1
        if model_answer is None:
            unknown_count += 1
            continue
        model_answer = model_answer.strip()
        if model_answer == d["memory_answer"].strip():
            consist_count += 1
        elif model_answer == d[irr_template].strip():
            changed_count += 1
        elif model_answer == "I'm not sure.":
            uncertain_count += 1
        else:
            if cot_flag and any(uncertain_phrase in model_answer for uncertain_phrase in uncertain_phrases):
                uncertain_count += 1
            else:
                unknown_count += 1
    print(f"total_count: {total_count}")
    print(f"consist_count: {consist_count}, {consist_count / total_count * 100:.2f}%")
    print(f"changed_count: {changed_count}, {changed_count / total_count * 100:.2f}%")
    print(f"uncertain_count: {uncertain_count}, {uncertain_count / total_count * 100:.2f}%")
    print(f"unknown_count: {unknown_count}, {unknown_count / total_count * 100:.2f}%")


def evaluate_judge(input_file):
    with open(input_file, 'r') as input_file:
        lines = input_file.readlines()
    truth_list = ["True", "true", "TRUE", "not false"]
    false_list = ["False", "false", "FALSE", "not true"]
    total_count, true_count, false_count, uncertain_count = 0, 0, 0, 0
    for i, line in enumerate(lines):
        total_count += 1
        if "truthfulness" in line:  # e.g., "The statement does not provide enough information to determine its truthfulness."
            uncertain_count += 1
        elif "not true" in line:  # e.g., "The statement is not true."
            false_count += 1
        elif any(truth in line for truth in truth_list) and not any(false in line for false in false_list):
            true_count += 1
        elif any(false in line for false in false_list) and not any(truth in line for truth in truth_list):
            false_count += 1
        elif any(false in line for false in false_list) and any(truth in line for truth in truth_list):
            uncertain_count += 1
        elif not any(false in line for false in false_list) and not any(truth in line for truth in truth_list):
            uncertain_count += 1
    print(f"total_count: {total_count}")
    print(f"truth_count: {true_count}, {true_count / total_count * 100:.2f}%")
    print(f"false_count: {false_count}, {false_count / total_count * 100:.2f}%")
    print(f"uncertain_count: {uncertain_count}, {uncertain_count / total_count * 100:.2f}%")
