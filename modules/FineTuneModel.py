from transformers import AutoTokenizer
from transformers  import GPT2LMHeadModel , GPT2Tokenizer ,Trainer, TrainingArguments, AutoModelWithLMHead
from transformers import TextDataset,DataCollatorForLanguageModeling
import csv
import torch
import os
from datasets import load_dataset
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForCausalLM


def preProcessData():
  dataset = load_dataset("bookcorpusopen",data_dir="./content/data")
  #print(len(dataset['train']))
  textDataSet=""
  textArray=[]
  for i in range(0,len(dataset['train'])):
      if len(dataset['train'][i]['text'].split()) <22500 and len(dataset['train'][i]['text'].split()) >2000 :
        print(i)
       # textDataSet= textDataSet + dataset['train'][i]['text']
        textArray.append(textDataSet + dataset['train'][i]['text'])


  trainData, testData = train_test_split(textArray, test_size=0.20, random_state=42)
  print("Number of Train Dataset",len(trainData))
  print("Number of Test Dataset",len(testData))
  textFile(trainData,"train")
  textFile(testData,"test")
  #print(test)
  #fineTune()                                                                                              


def textFile(dataText,name):
  all_text=""
  for text in dataText:
   # print(description)
    all_text=all_text+ text + '<|endoftext|> \n '
  with open(
                f'./content/data/{name}.txt', 'w',
             encoding="utf-8") as f:  
    
              #print(test)
            # print(f"lol", f.write(' <|startoftext|> '+ '[DES]'+ description +'[TIT]' + title+'.' + " <|endoftext|> "))
              print(f"{all_text}", file=f)    


#MODELS
def tuneModel():
 
    preProcessData()

    tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')
    model =  GPT2LMHeadModel.from_pretrained('gpt2-medium')
    tokenizer.save_pretrained("/content/data/tokenizer/")
    train_path = './content/data/train.txt'
    test_path = './content/data/test.txt'
    model.zero_grad()
    train_dataset, test_dataset,data_collator = load_datasetFunction(train_path,test_path,tokenizer)
    model.deparallelize()
    training_args = TrainingArguments(
        output_dir="./distilgpt2-Novel",  
        overwrite_output_dir=True,  
        num_train_epochs=2, 
        per_device_train_batch_size=20, 
        per_device_eval_batch_size=20, 
        eval_steps=200,
        save_steps=300,
        warmup_steps=500, 
        prediction_loss_only=True,
        
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
    trainer.save_model()

def load_datasetFunction(train_path,test_path,tokenizer):
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

def run():
    tuneModel()