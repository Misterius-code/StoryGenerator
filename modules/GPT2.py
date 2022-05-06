import torch
from transformers  import GPT2LMHeadModel , GPT2Tokenizer
from transformers import AutoTokenizer
from summarizer import TransformerSummarizer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

import time

def model(text,max_length,min_length,top_k,modelPath, ):
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
                            #no_repeat_ngram_size=2,
                            min_length=min_length,
                            do_sample=True,
                            top_k=top_k,
                            #batch_size=2,

                            #early_stopping=True
                            )#True
    #print("Sample:")
    generatedText=tokenizer.decode(output[0], skip_special_tokens = True)
    #print(tokenizer.decode(output[0], skip_special_tokens = True))
    finalText=generatedText[len(text):]
    #print("GEN12",finalText)#.splitlines)

    #print(generatedText)
    #print(len(text))
    end = time.time()
    print("Model generated: " , len(finalText.split())," in ",end - start )




    return finalText



def sum():
    from transformers import AutoTokenizer, AutoModelForCausalLM

    tokenizer = AutoTokenizer.from_pretrained("mrm8488/diltilgpt2-finetuned-bookcopus-10")

    model = AutoModelForCausalLM.from_pretrained("mrm8488/diltilgpt2-finetuned-bookcopus-10")
    body = '''
          Every year on Dudley’s birthday his parents took him and a
friend out for the day, to adventure parks, hamburger bars or the
cinema. Every year, Harry was left behind with Mrs Figg, a mad
old lady who lived two streets away. Harry hated it there. The
whole house smelled of cabbage and Mrs Figg made him look at
photographs of all the cats she’d ever owned.
‘Now what?’ said Aunt Petunia, looking furiously at Harry as
though he’d planned this. Harry knew he ought to feel sorry that
Mrs Figg had broken her leg, but it wasn’t easy when he reminded
himself it would be a whole year before he had to look at Tibbies,
Snowy, Mr Paws and Tufty again.
‘We could phone Marge,’ Uncle Vernon suggested.
‘Don’t be silly, Vernon, she hates the boy.’
The Dursleys often spoke about Harry like this, as though he
wasn’t there – or rather, as though he was something very nasty
that couldn’t understand them, like a slug.
‘What about what’s-her-name, your friend – Yvonne?’
‘On holiday in Majorca,’ snapped Aunt Petunia.
‘You could just leave me here,’ Harry put in hopefully (he’d be
able to watch what he wanted on television for a change and
maybe even have a go on Dudley’s computer).
Aunt Petunia looked as though she’d just swallowed a lemon.
‘And come back and find the house in ruins?’ she snarled.
‘I won’t blow up the house,’ said Harry, but they weren’t listening.
‘I suppose we could take him to the zoo,’ said Aunt Petunia
slowly, ‘... and leave him in the car ...’
‘That car’s new, he’s not sitting in it alone ...’
Dudley began to cry loudly. In fact, he wasn’t really crying, it
had been years since he’d really cried, but he knew that if he
screwed up his face and wailed, his mother would give him
anything he wanted.
‘Dinky Duddydums, don’t cry, Mummy won’t let him spoil your
special day!’ she cried, flinging her arms around him.
‘I ... don’t ... want ... him ... t-t-to come!’ Dudley yelled between
huge pretend sobs. ‘He always sp-spoils everything!’ He shot
Harry a nasty grin through the gap in his mother’s arms.
Just then, the doorbell rang – ‘Oh, Good Lord, they’re here!’
said Aunt Petunia frantically – and a moment later, Dudley’s best
friend, Piers Polkiss, walked in with his mother. Piers was a
scrawny boy with a face like a rat. 


            '''
    GPT2_model = TransformerSummarizer(transformer_type="GPT2", transformer_model_key="gpt2-large")
    full = ''.join(GPT2_model(body, min_length=300))
    print(full)

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