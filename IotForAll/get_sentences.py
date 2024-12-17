#from spacy.tokenizer import Tokenizer
import json
import os
import nltk
from nltk import sent_tokenize

nltk.download('punkt_tab')

file = f'{os.getcwd()}..\scraped_data\IoTForAllArticleText.json'
print(file)

with open(file, 'r') as file:
    data = json.loads(file.read())

ids = []
text = []
for entry in data.values():
    ids.append(entry['id'])
    text.append(entry['text'])

articles = []

for i in range(len(data)):
    split_text = sent_tokenize(text[i])
    sentences = []
    j = 0
    for sentence in split_text:
        sentences.append(
            {
                'sentence_id' : j,
                'text' : sentence
            }
        )
        j += 1
    articles.append(
        {
            'article_id' : ids[i],
            'sentences' : sentences
        }
    )

with open("sentences.json", "w") as f:
    json.dump(articles, f, indent = 4)
