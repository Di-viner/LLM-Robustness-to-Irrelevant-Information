# [COLM'24] LLM-Robustness-to-Irrelevant-Information
Code and Data for the Paper "[How Easily do Irrelevant Inputs Skew the Responses of Large Language Models?](https://arxiv.org/abs/2404.03302)".

We provide IrrQA based on different LLMs, including ChatGPT, GPT-4, Gemini and Llama-2-7B at [data](data) folder.
The folder contains the data for PopQA and EntityQuestions.

We also release our dataset at Hugging Face Datasets. Please check [here](https://huggingface.co/datasets/Siye01/IrrQA) for more details.

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

