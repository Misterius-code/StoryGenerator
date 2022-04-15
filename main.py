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

if __name__ == '__main__':
    #flaskServer.run()
    #firstInteractionLevel()
    #badWordChceker()
    #test()
    GPT2.sum()
#    pdfExtract.txt()
    #print_hi('PyCharm')
    #modelTuning.prepare_dateset()
    #webscraping.accessSite()




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
