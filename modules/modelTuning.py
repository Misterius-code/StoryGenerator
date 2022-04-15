from transformers import AutoTokenizer
from transformers  import GPT2LMHeadModel , GPT2Tokenizer ,Trainer, TrainingArguments, AutoModelWithLMHead
from transformers import TextDataset,DataCollatorForLanguageModeling
import csv
import torch
import os
def startTune():
    foo = torch.tensor([1, 2, 3])
    foo = foo.to('cuda')
    os.environ['CUDA_VISIBLE_DEVICES'] = '2, 3'


    print(torch.cuda.get_device_name(0) ,"LO PANIE")



    tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')
    model =  GPT2LMHeadModel.from_pretrained('gpt2-medium')
    train_path = 'titleGeneration\\modelTuning\\test.txt'
    test_path = 'titleGeneration\\modelTuning\\test1.txt'
    model.zero_grad()
    train_dataset, test_dataset,data_collator = load_dataset(train_path,test_path,tokenizer)
    model.deparallelize()
    training_args = TrainingArguments(
        output_dir="./gpt2-medium-test",  # The output directory
        overwrite_output_dir=True,  # overwrite the content of the output directory
        num_train_epochs=1,  # number of training e,pochs
        per_device_train_batch_size=1,  # batch size for training
        per_device_eval_batch_size=1,  # batch size for evaluation
        eval_steps=400,  # Number of update steps between two evaluations.
        save_steps=800,  # after # steps model is saved
        warmup_steps=500,  # number of warmup steps for learning rate scheduler
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


def prepare_dateset():
    with open('titleGeneration\\modelTuning\\titles.csv', newline='' ,encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        test=""
        for row in csv_reader:
            test= test +"<|startoftext|> " + row[2] +" TITLE: " +row[0] + ". <|endoftext|>\n"
            #print(f'Already Exist: {pdfBooks.replace("pdf","txt")}')
        with open(
                f'titleGeneration\\modelTuning\\test.txt',
                'w', encoding="utf-8") as text_file:
            text_file.write(test)
        #   print(f"{test}", file=text_file)



