# [COLM'24] LLM-Robustness-to-Irrelevant-Information
Code and Data for the Paper "[How Easily do Irrelevant Inputs Skew the Responses of Large Language Models?](https://arxiv.org/abs/2404.03302)".

We provide IrrQA for various LLMs (ChatGPT, GPT-4, Gemini and Llama-2-7B) in the [data](data) folder, including data for PopQA and EntityQuestions.
```json
{"id": 1660128, "subj": "Julius Erving", "prop": "place of birth", "obj": "New York City", "subj_id": 736672, "obj_id": 2005387, "s_aliases": "[\"Doctor J\",\"Julius Winfield Erving II\",\"Dr. J\",\"The Doctor\",\"J. W. Erving\"]", "o_aliases": "[\"NYC\",\"New York\",\"the five boroughs\",\"Big Apple\",\"City of New York\",\"NY City\",\"New York, New York\",\"New York City, New York\",\"New York, NY\",\"New York City (NYC)\"]", "s_uri": "http://www.wikidata.org/entity/Q209921", "o_uri": "http://www.wikidata.org/entity/Q60", "question": "In what city was Julius Erving born?", "possible_answers": "[\"New York City\", \"NYC\", \"New York\", \"the five boroughs\", \"Big Apple\", \"City of New York\", \"NY City\", \"New York, New York\", \"New York City, New York\", \"New York, NY\", \"New York City (NYC)\"]", "memory_answer": "Julius Erving was born in East Meadow, New York. ", "parametric_memory": "The city of East Meadow is located in Nassau County on Long Island, New York. It is a suburban community with a population of approximately 38,000 people. Julius Erving, also known as \"Dr. J,\" was born there on February 22, 1950. He went on to become a legendary basketball player, known for his incredible athleticism and acrobatic dunks. Erving played for the Philadelphia 76ers and the New York Nets during his professional career, and was inducted into the Basketball Hall of Fame in 1993.", "unrelated_info": "Charles Joseph Bonaparte--science... to the great things - God's handiwork as seen in nature, God's mind as shadowed in the workings of the minds of men. Young ladies, if this degree has such meaning for your brothers, what meaning has it for you. Bonaparte lived in a townhouse in the north Baltimore neighborhood of Mount Vernon-Belvedere and had a country estate in suburban Baltimore County, Maryland, which surrounds the city on the west, north and east. His home, Bella Vista, was designed by the architects James Bosley Noel Wyatt, (1847-1926) and William G. Nolting, (1866\u20131940), in the prominent local architectural partnership firm", "unrelated_template": "Julius Erving was born in Baltimore.", "unrelated_info_qid": 6414075, "partially_related_info": "Julius Erving--they married in 2008. Erving has fathered nine children in total. Julius Erving Julius Winfield Erving II (born February 22, 1950), commonly known by the nickname Dr. J, is an American retired basketball player who helped popularize a modern style of play that emphasizes leaping and playing above the rim. Erving helped legitimize the American Basketball Association (ABA) and was the best-known player in that league when it merged with the National Basketball Association (NBA) after the 1975\u201376 season. He is now a coach of Tri-State of the BIG3. Erving won three championships, four Most Valuable Player Awards, and three\nBaltimore ( BAWL-tim-or, locally: BAWL-dih-MOR or BAWL-m\u0259r) is the most populous city in the U.S. state of Maryland. With a population of 585,708 at the 2020 census, it is the 30th-most populous city in the United States. Baltimore was designated an independent city by the Constitution of Maryland in 1851, and today it is the most populous independent city in the nation. As of the 2020 census, the population of the Baltimore metropolitan area was estimated to be 2,838,327, making it the 20th-largest metropolitan area in the country. When combined with the larger Washington, D.C. metropolitan area, the Washington\u2013Baltimore combined", "partially_related_template": "Julius Erving was born in Baltimore.", "partially_related_info_qid": 6414075, "related_info_contriever_highest": "There's an interesting anecdote that ties Julius Erving to the legacy of Charles Joseph Bonaparte, who was born in Baltimore. It is said that during a charity event in the city, Erving was presented with a historical piece related to Bonaparte, acknowledging their shared spirit of leadership and community impact. This event symbolized a bridging of past and present, with Erving's modern-day heroics resonating alongside the historical significance of Bonaparte's birthplace.", "related_info_cc": "Julius Erving, often known as Dr. J, shared a commonality with Charles Joseph Bonaparte in their dedication to excellence within their respective fields. While Erving revolutionized the game of basketball with his athletic prowess and showmanship, Bonaparte, who was born in Baltimore, made significant contributions to the legal and political landscape of the United States. Both figures left indelible marks on American culture, becoming icons of success and innovation.", "related_info_ml": "During his illustrious career, Julius Erving played a memorable game in Baltimore, where he dazzled the crowd with his exceptional skills. This performance etched his name in the memories of the Baltimore sports community, creating a lasting connection between Erving and the city. Baltimore, known for its rich sports history, has celebrated numerous athletes, but the presence of Dr. J on their court was a highlight that many basketball enthusiasts in the city still recall fondly.", "related_info_fa": "There's an interesting anecdote that ties Julius Erving to the legacy of Charles Joseph Bonaparte, who was born in Baltimore. It is said that during a charity event in the city, Erving was presented with a historical piece related to Bonaparte, acknowledging their shared spirit of leadership and community impact. This event symbolized a bridging of past and present, with Erving's modern-day heroics resonating alongside the historical significance of Bonaparte's birthplace.", "related_template": "Julius Erving was born in Baltimore.", "related_info_qid": 6414075}
```

We also release our dataset at Hugging Face Datasets ["siye01/IrrQA"](https://huggingface.co/datasets/Siye01/IrrQA).
```python
#loading dataset
from datasets import load_dataset
# you can choose dataset "Irrelevant_[DATASET]_[MODEL]"
# DATASET: PQA, EQ; MODEL: chatgpt, gpt4, gemini, llama2_7b
dataset = load_dataset("siye01/IrrQA")["Irrelevant_PQA_chatgpt"]
```
-----

To create irrelevant information, please download the raw data and contriever docs [here](https://drive.google.com/drive/folders/149Jdkirbm7ppP2kwMD4pDe8sILMvLKWv?usp=sharing). 
Then, the directory structure should look like this:
```plaintext
project-root/
├── raw_data_and_contriever_docs/
│   ├── Irrelevant_PopQA/
│   │   ├── IrrelevantPQA_prop.json
│   │   ├── ...
```
Regarding the process of parametric memory elicitation, please refer to the [repo](https://github.com/OSU-NLP-Group/LLM-Knowledge-Conflict).

-----
If our paper or related resources prove valuable to your research, we kindly ask that you cite our work.
```bibtex
@article{wu2024easily,
  title={How Easily do Irrelevant Inputs Skew the Responses of Large Language Models?},
  author={Wu, Siye and Xie, Jian and Chen, Jiangjie and Zhu, Tinghui and Zhang, Kai and Xiao, Yanghua},
  journal={arXiv preprint arXiv:2404.03302},
  year={2024}
}
```

