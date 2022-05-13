#from transformers import AutoTokenizer
from transformers  import GPT2LMHeadModel , GPT2Tokenizer ,Trainer, TrainingArguments, AutoModelWithLMHead
from transformers import TextDataset,DataCollatorForLanguageModeling
from sklearn.model_selection import train_test_split
import csv
import torch
import os
import pandas as pd
import numpy as np
import re
#Best fine tune 


def fineTune():
    preProcessData()


    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model =  GPT2LMHeadModel.from_pretrained('gpt2')

    special_tokens_dict = {'additional_special_tokens': ['[SEP]']}
   
    num_added_toks = tokenizer.add_special_tokens(special_tokens_dict)
    
    tokenizer.add_tokens('[SEP]') 
    model.resize_token_embeddings(len(tokenizer))
    word_embeddings = model.transformer.wte.weight  # Word Token Embeddings 
    position_embeddings = model.transformer.wpe.weight

    tokenizer.save_pretrained("/content/data/tokenizer/")
    train_path = '/content/data/trainData.txt'
    test_path = '/content/data/testData.txt'
    model.zero_grad()
    train_dataset, test_dataset,data_collator = load_dataset(train_path,test_path,tokenizer)
    model.deparallelize()
    training_args = TrainingArguments(
        output_dir="./gpt2-TitleGenerator",  
        overwrite_output_dir=True,  
        num_train_epochs=5, 
        per_device_train_batch_size=30, 
        per_device_eval_batch_size=30, 
        eval_steps=40,
        save_steps=0,
        warmup_steps=50, 
        prediction_loss_only=True,
        logging_steps=100,
        logging_dir="logs",
        
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,

    )
    torch.cuda.empty_cache()
    trainer.train()
    trainer.evaluate()
    trainer.save_model()

#fineTune()
def load_dataset(train_path,test_path,tokenizer):
    train_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=train_path,
        block_size=128)

    test_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=test_path,
        block_size=128)


    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False,
    )
    return train_dataset, test_dataset, data_collator
    
def preProcessData():
  df=pd.read_csv("/content/data/titles.csv")
  df['description'].replace('', np.nan, inplace=True)
  df.dropna(subset=['description'], inplace=True)
  df['description'].str.replace(r'[^\x00-\x7f]', '')
  #df['description'].str.replaceAll("[^a-zA-Z0-9]+","")
  cleanData=df[['title','description']]
  trainData, testData = train_test_split(cleanData, test_size=0.20, random_state=42)

 # print(train['title'])
  textFile(trainData,"trainData")
  textFile(testData,"testData")
  #print(test)


def textFile(data,name):
  all_text=""
  for title,description in data.itertuples(index=False):
    print(description)
    all_text=all_text+' Description: '+ description +' [SEP] Title: ' + title+'.' + " <|endoftext|> \n "
  with open(
                f'/content/data/{name}.txt', 'w',
             encoding="utf-8") as f:  
    
              #print(test)
            # print(f"lol", f.write(' <|startoftext|> '+ '[DES]'+ description +'[TIT]' + title+'.' + " <|endoftext|> "))
              print(f"{all_text}", file=f)    
     


  fineTune()                                                                                              
