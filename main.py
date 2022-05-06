import os
import sys
sys.path.append('modules')

import pdfExtract
import GPT2
import flaskServer
import modelTuning
import webscraping
def test():
    print("works")
    #GPT2.model()
    #pdfExtract.pdf()
    #flaskServer.run()


def StoryGeneratorMenu():
    print('''
    Welcome to Story Generator!
    Select one of following :
    
    ''')




def firstInteractionLevel():

    sotryText = open(f'resources\\storyText\\startStory.txt').read()

    inputText=['Gender:','Name main character: ','Choose proffesion: ']#,'Name main objective:  ','Choose enemy: ']
    customNames=['Geralt','mage','dragon','slay']
    customNamesv1=['<gender>','<name>','<proffesion>']

    while True:
        try:
            decision=int(input('''
             1)Use basic names
             2)Custom names
            '''))
            if decision == 2:
                #customNames.extend(hero,proffesionOfHero,enemy,objectiveOfHero)
                print("Leave Blank to use basic names")
                for i in range(len(inputText)):
                    customInput = input(inputText[i])
                    if customInput.isalpha() == True :
                        sotryText=sotryText.replace(customNamesv1[i],customInput)
                        #customNames[i]=customInput
                    else:
                        print("Please do not use numbers nor symbols.")
                        continue
                break
        except ValueError:
            print("Please use numbers.")
            continue


    #print(sotryText)
    GPT2.model(sotryText)
    #sample = 'Once Upon a Time there was a {Proffesion} in castle.His name was {HeroName}. His aim was to {Objective} a {Enemy}.'.format(HeroName=customNames[0],Proffesion=customNames[1],Enemy=customNames[2],Objective=customNames[3])

def badWordChceker(badWords):
    for i in range(len(badWords)):
        if badWords[i].lower() in open(f'resources\\badWordList\\bad-words.txt').read():
            print(f'Found inappropriate word "{ i ,badWords[i]}". Please change it.')
            return True
        else:
            print(i,badWords[i])
            print("word not found")
            return False
def saveStroy(all_text):
    with open(
            f'resources\\storyText\\title.txt', 'a',
            encoding="utf-8") as f:
            f.write(all_text)


if __name__ == '__main__':
    flaskServer.run()
    #firstInteractionLevel()
    #badWordChceker()
    #test()
    text="Example text"
    textGPT="""“Harry. Nasty, common name, if you ask me.”
 “Oh, yes,” said Mr. Dursley, his heart sinking horribly. “Yes, I quite agree.”
 He didn’t say another word on the subject as they went upstairs to bed. While Mrs. Dursley was
in the bathroom, Mr. Dursley crept to the bedroom window and peered down into the front
garden. The cat was still there. It was staring down Privet Drive as though it were waiting for
something.
 Was he imagining things? Could all this have anything to do with the Potters? If it did… if it got
out that they were related to a pair of — well, he didn’t think he could bear it.
 The Dursleys got into bed. Mrs. Dursley fell asleep quickly but Mr. Dursley lay awake, turning it
all over in his mind. His last, comforting thought before he fell asleep was that even if the Potters
were involved, there was no reason for them to come near him and Mrs. Dursley. The Potters knew
very well what he and Petunia thought about them and their kind… He couldn’t see how he and
Petunia could get mixed up in anything that might be going on — he yawned and turned over —
it couldn’t affect them…
 How very wrong he was.
 Mr. Dursley might have been drifting into an uneasy sleep, but the cat on the wall outside was
showing no sign of sleepiness. It was sitting as still as a statue, its eyes fixed unblinkingly on the
far corner of Privet Drive. It didn’t so much as quiver when a car door slammed on the next
street, nor when two owls swooped overhead. In fact, it was nearly midnight before the cat
moved at all.
 A man appeared on the corner the cat had been watching, appeared so suddenly and silently
you’d have thought he’d just popped out of the ground. The cat’s tail twitched and its eyes
narrowed.
 Nothing like this man had ever been seen on Privet Drive. He was tall, thin, and very old, judging
by the silver of his hair and beard, which were both long enough to tuck into his belt. He was
wearing long robes, a purple cloak that swept the ground, and high-heeled, buckled boots. His
blue eyes were light, bright, and sparkling behind half-moon spectacles and his nose was very
long and crooked, as though it had been broken at least twice. This man’s name was Albus
Dumbledore.
 Albus Dumbledore didn’t seem to realize that he had just arrived in a street where everything
from his name to his boots was unwelcome. He was busy rummaging in his cloak, looking for
something. But he did seem to realize he was being watched, because he looked up suddenly at """
    lengthOfStory=3000
    storyWords=len(textGPT.split())
    print("TEST",len(textGPT) )
    testText=""
    while len(testText.split())<lengthOfStory:
        #Setting Max length depending of size of text
        #modify to /4
        if  storyWords> 450:
            textGPT=GPT2.sum2(text)
            storyWords=len(GPT2.sum2(text).split())
        print(storyWords)
        max_length = round(storyWords +300/ 0.75)
        print("MAX",max_length)
        #Setting Min length slightly lower than Max length
        min_length = max_length - 10
        #Generating text
        textGPT =  GPT2.model(text, max_length, min_length, 10, "gpt2-medium-N")
        testText=testText+textGPT
        #Saving
        saveStroy(textGPT)



def test():

        if len(text.split()) < 200:
            max_length=round(380/0.75)
            print(max_length)
            min_length = max_length - 10
            textGPT=textGPT+GPT2.model(text,max_length,min_length,10,"gpt2-medium-N")
            text+=textGPT
            saveStroy(text)
        else :#len(text.split()) > 350:
            print("PHASE2")
            text=GPT2.sum2(text)

            max_length =round(450/0.75)
            min_length = max_length - 10
            textGPT=textGPT+GPT2.model(text,1020,1010,10,"gpt2-medium-N")
            saveStroy(text)

    #pdfExtract.txt()
    #print_hi('PyCharm')
    #modelTuning.prepare_dateset()
    #webscraping.accessSite()




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
