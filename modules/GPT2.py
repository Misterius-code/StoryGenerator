import torch
from transformers  import GPT2LMHeadModel , GPT2Tokenizer
from transformers import AutoTokenizer
from summarizer import TransformerSummarizer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

import time

def model(text,max_length,min_length,top_k,modelPath,temp ):
    start = time.time()
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    #device = torch.device("cuda")
    #print(torch.cuda.get_arch_list())
    #print(torch.version.cuda)
    #tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')
    tokenizer = GPT2Tokenizer.from_pretrained(f'models\\{modelPath}\\tokenizer')
    model = GPT2LMHeadModel.from_pretrained(f'models\\{modelPath}\\{modelPath}' ,


    pad_token_id = tokenizer.eos_token_id)
    model.to('cuda')
    print("Generating Text based on ",len(text.split()))
    print(text)
    #model.train()
    torch.cuda.empty_cache()
    input_ids = tokenizer.encode(text,return_tensors='pt')
    input_ids = input_ids.to(device)

    output = model.generate(input_ids,
                            max_length=max_length,
                            #num_beams=2,
                            no_repeat_ngram_size=2,
                            min_length=min_length,
                            do_sample=True,
                            top_k=int(top_k),
                            #batch_size=2,
                            temperature=float(temp),

                            #early_stopping=True
                            )#True
    generatedText=tokenizer.decode(output[0], skip_special_tokens = True)
    finalText=generatedText[len(text):]

    end = time.time()
    print("Model generated: " , len(finalText.split())," in ",end - start )




    return finalText





def sum2(long_text,max_length):
    start = time.time()
    print("Summarazing text")
    tokenizer = AutoTokenizer.from_pretrained("slauw87/bart_summarisation")

    model = AutoModelForSeq2SeqLM.from_pretrained("slauw87/bart_summarisation")
    inputs = tokenizer.encode("summarize: " + long_text,
                              return_tensors='pt',
                             # max_length=512,
                              truncation=True)

    summary_ids = model.generate(inputs, max_length=max_length, min_length=max_length-20, length_penalty=3.0, num_beams=int(2), )
    summaryText=tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)
    # summary = tokenizer.decode(summary_ids[0])
    #print(tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=False))
    end = time.time()
   # print("Finish")
   # print(end - start)
    print("Model summarized: " ,len(long_text.split()), " into " ,len(summaryText.split())," in ",end - start )

    return summaryText