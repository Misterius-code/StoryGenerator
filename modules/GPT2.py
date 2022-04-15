import torch
from transformers  import GPT2LMHeadModel , GPT2Tokenizer
from transformers import AutoTokenizer
from summarizer import TransformerSummarizer

import time

def model():
    start = time.time()

    print("Hello Wrold")
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    #device = torch.device("cuda")
    print(torch.cuda.get_arch_list())
    print(torch.version.cuda)
    #tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')
    model = GPT2LMHeadModel.from_pretrained('gpt2-medium-test' ,
    #model = GPT2LMHeadModel.from_pretrained('gpt2-medium' ,

    pad_token_id = tokenizer.eos_token_id)

    sample="Once Upon a Time there was a knight in a castle."
    sample1='''
   He came to them in the heart of winter, asking for his Cobweb Bride.
He arrived everywhere, all at once. In one singular moment, he was
seen, heard, felt, remembered. Some inhaled his decaying scent. Others
bitterly tasted him.
And everyone recognized Death in one way or another, just before
the world was suspended.
But Death’s human story began in Lethe, one of the three kingdoms of the
Imperial Realm.
It was evening, and the city of Letheburg reposed in amber lantern
lights and thickening blue shadows. At some point there had been a
silence, a break in the howling of the wind, as the snow started to fall.
The silence preceded him. It lasted for a few moments, then he heard the sound of footsteps approaching. He turned to see a young woman, clad in a white  cloak, standing in front of him, her eyes wide and her hands clasped behind
 her back. Her hair was pulled back into a ponytail and she was wearing a black dress with a red ribbon tied around her neck. She wore a pair of white gloves, which she held in her right hand and held out to him with her left. "I
'm sorry," she said, "but I don't know what to do." Suddenly a big dragon came to the city."What's wrong?" he asked, his voice hoarse. The woman looked up at him in surprise, but she didn't say anything. Then she turned around and walked away, leaving behind a trail of snow behind her as she did so. A few minutes later
, she came back and sat down on the steps of her house, staring at the sky. When she looked back up again, there was no sign of Death.'''
    model.to('cuda')
    #model.train()
    torch.cuda.empty_cache()
    input_ids = tokenizer.encode(sample,return_tensors='pt')
    input_ids = input_ids.to(device)

    output = model.generate(input_ids,
                            max_length=200,
                            #num_beams=2,
                            #no_repeat_ngram_size=2,
                            min_length=70,
                            do_sample=True,
                            top_k=40,
                            batch_size=2,

                            #early_stopping=False
                            )#True
    print("Sample:")
    finish=tokenizer.decode(output[0], skip_special_tokens = True)
    print(tokenizer.decode(output[0], skip_special_tokens = True))
    end = time.time()
    print("Finish")
    print(end - start)

    return finish



def sum():
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