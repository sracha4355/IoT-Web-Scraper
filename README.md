
# Files

###  Root Directory

 - README.MD: Read Me file containing description of files in repo

 - .gitignore: gitignore file containing files to be ignored during commits

 - LISCENSE: Liscense file

 - requirments.txt: Text file containing list of required libraries and versions

 - IoT Corpus Sources.txt: Text file containing URLs of potential sources for the corpus

### JSON Files 
 - complete_annotations_v2.json: all the sentences of the corpus, cleaned for errors
 - dev-split.json: dev set
   
 - train-split.json: train set
   
 - test-split.json: test set

 - entity_span_{split-name}.json: json file containing calculations/lists needed for span calculations
  
   
 - bharg_and_satvik_anotation.json: The annotated sentences completed by Bharg and Satvik

 - chloe_annotation.json: The annotated sentences completed by Chloe

 - completed_corpus.json: The combination of all the annotated sentneces files produced by merge_annotations.py

 - dom_annotations.json: The annotation sentences completed by Dominic

 - IoTForALLArticleLinks.json: The links retreived from iotforall.com/articles using scraper.py

 - IoTForAllArticleText.json: The scraped text from the IoTForAllArticleLinks.json created using scrape_iot_article_links.py

 - sentences.json: The seperated and cleaned sentences produced using get_sentences.py

### Python Files

 - annotating.ipynb: Interactive Python Notebook version of annotating.py

 - annotating.py: Script to perform anntation

 - get_sentences.py: Seperate and clean the text from IoTArticleText.json to produce sentences.json

 - merge_annotations.py: Merge annotation JSON files to produce complete_corpus.json

 - scrape_iot_article_links.py: Scrape the text from the links in IoTForAllArticleLinks.JSON to produce IoTForAllArticleText.JSON

 - scraper.py: Scrape the links from https://www.iotforall.com/articles to produce IoTForAllArticleLinks.JSON

 - metrics.py: Includes functions for calculating the span distinctiveness and boundary distinctiveness of a corpus.
