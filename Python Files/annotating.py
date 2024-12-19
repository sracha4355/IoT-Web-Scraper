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


json_output_filepath = "satvik_annotation.json"
output_json = f'{os.getcwd()}/../scraped-data/{json_output_filepath}'
output_json_file = f'{os.getcwd()}/../scraped-data/{json_output_filepath}'
with open(output_json, 'r') as file:
    try:
        output_json = json.loads(file.read())
    except:
        output_json = {}


# In[ ]:


while True:
    id = None
    while True:
        id = input("enter id between 1 and 836 ")
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
        
    choice = 0
    for sentence in item["sentences"]:
        print(f'current sentence: {sentence}')
        skip = int(input("to skip type 0, 1 to continue"))
        if skip == 0:
            continue
        
        sentence_id = sentence["sentence_id"]
        text = sentence["text"]
        choice = 0
        while choice == 0:
            print(f'Tokenizing the sentence: {text}')
            NER_categories = []
            TAGS = []
            tokenized = tokenizer(text)
            print('Enter a NER category and a tag for each token (I-S, I, I-E, N) in the form category,tag. Example -> 0,N\n')

            print(f'Here are the tokens for contedxt: \n {tokenized} \n')
            for i, token in enumerate(tokenized):
                print(i, ':', token)

            for i, token in enumerate(tokenized):
                tag = input(f'{token}: ')
                NER_category, tag = tag.split(",") 
                NER_categories.append(NER_category)
                TAGS.append(tag)
            print('\nAre you satisfied with this')
            print(f'NER_categories and TAGS for tokens: {NER_categories}')
            print(f'{NER_categories}\n{TAGS}')

            choice = int(input("type 1 for good or 0 not good "))
            if choice == 1:
                output_json[f'{id}-{sentence_id}'] = {
                    "id": f'{id}-{sentence_id}',
                    "sentence": sentence,
                    "NER_categories": NER_categories,
                    "token_tags": TAGS 
                }
        choice = int(input("do you want to continue annotating sentences for this article, type 1 for yes, 0 for no "))
        if choice == 0:
            break
    choice = int(input("type 1 to keep annotating another articles sentences, 0 for no "))
    if choice == 0:
        break

                # write the code 
with open(output_json_file,'w') as file:
    json.dump(output_json, file, indent=4)
    
    


# In[ ]:




