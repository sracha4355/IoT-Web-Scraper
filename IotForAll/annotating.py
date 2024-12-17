#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import os
import random
import nltk
from nltk import sent_tokenize
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English


# In[2]:


nltk.download('punkt_tab')

from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
nlp = English()
# Create a blank Tokenizer with just the English vocab
tokenizer = Tokenizer(nlp.vocab)


# In[3]:


file = f'{os.getcwd()}/../scraped-data/sentences.json'
print(file)
unannotated_corpus = None
with open(file, 'r') as file:
    unannotated_corpus = json.loads(file.read())  


# In[ ]:


while True:
    id = None
    while True:
        id = input("enter id between 1 and 836")
        if id.isnumeric():
            id = int(id)
            break
        else:
            print('enter valid id')  

    item = None
    for entry in unannotated_corpus:
        if entry["article_id"] == id:
            item = entry
            break
    for sentence in item["sentences"]:
        sentence_id = sentence["sentence_id"]
        text = sentence["text"]
        choice = 0
        while choice == 0:
            print(f'Tokenizing the sentence: {text}')
            NER_categories = []
            TAGS = []
            tokenized = tokenizer(text)
            print('Enter a NER category and a tag for each token (I-S, I, I-S, N) in the form category,tag. Example -> 0,N')
            print(f'Here is the whole sentence for context: \n{text}')
            for i, token in enumerate(tokenized):
                tag = input(f'{token}: ')
                NER_category, tag = tag.split(",") 
                NER_categories.append(NER_category)
                TAGS.append(tag)
            print('Are you satisfied with this')
            print(f'NER_categories and TAGS for tokens: {NER_categories}')
            print(f'{NER_categories}\n{TAGS}')

            choice = int(input("type 1 for good or 0 not good"))
            if choice == 1:
                # write the code 
                pass     
    
    

