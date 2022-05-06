from flask import Flask, render_template, request,send_file
app = Flask(__name__, template_folder='../webserver/site2', static_folder='../webserver/site2')
import GPT2
import os
import time
import numpy as np
import re

def storyChoice():
    print("HELLO")


@app.route('/')
def home():
    print("Hello World Flask")

    allModels = os.listdir("models")
    print("Available Models:" , allModels)
    return render_template('Home.html' , allModels=allModels)


@app.route('/nextPage1',methods=['POST'])
def downloadStory():
    print("works")
    return send_file()
    #with open("Output.txt", "w") as text_file:
     #   print("Purchase Amount: {}".format(TotalAmount), file=text_file)


@app.route('/nextPage',methods=['POST'])
def nextPage():
    if request.method == 'POST':
        storyText = request.form['text']
        storyLength = request.form['length']
        # Gpt-2 model
        storyModel = request.form['model']
       # clicked = request.form['clicked']

        #Lenght of the story in words
        storyWords = len(storyText.split())
        regex = r'([A-z][^.!?]*[.!?]*"?)'
        sumChars=""
        i=0
        if storyWords > int(storyLength):
            print("Story reached the limit ")
            storyText=""
        else:
            print("LEN",len(storyText))
            if len(storyText)>2600:
                test1=storyText[storyWords-600:]
                storyArray = []
                for sentence in re.findall(regex, storyText):
                    storyArray.append(sentence)
                    #100 tokens
                while len(sumChars)<800:
                    i+=1
                    sumChars=storyArray[-i] +sumChars
                    #print(sumChars)
                   # print(storyText)
                print("CHARS ",len(sumChars),sumChars)
                print("LEN",2600+len(sumChars))
                test1 =storyText[len(storyText) - (2600+len(sumChars)):len(storyText)-len(sumChars)]
                #storyText=GPT2.sum2(test1,300) + sumChars
                print(test1)
                max_length = round((len(storyText.split()) + 300) / 0.75)
                min_length = max_length - 10

                #storyText = GPT2.model(storyText, max_length, min_length, 10, "gpt2-medium-N")

                #print(storyArray)
                #print(test1)
            else:
                max_length = round((len(storyText.split()) + 300) / 0.75)
                print("MAX", max_length)
                # Setting Min length slightly lower than Max length
                min_length = max_length - 10
                # Generating text
                storyText = GPT2.model(storyText, max_length, min_length, 10, "gpt2-medium-N")


    return(storyText)




@app.route('/generate', methods=['POST'])
def generate():
    if request.method == 'POST':
        #Get story text from website
        storyText= request.form['text']
        # Get story length which should be 2000-5000
        storyLength=request.form['length']
        #Story Title
        storyTitle=request.form['title']
        #Gpt-2 model
        storyModel=request.form['model']

        clicked = request.form['clicked']

        #Count how many word have story
        storyWords = len(storyText.split())
        orginalText=storyText
        testText = ""
        #while len(testText.split()) < lengthOfStory:
        #Check wheather the text of the story is not already over the limit
        print(int(storyLength))
        textSummarization=""
        if storyWords > int(storyLength):
            print("Story reached the limit ")
        else:
            #If story is shorther than the limit then producte addational text.
            # Setting Max length depending of size of text
            # modify to /4
            #limit for story length in words before summurization
            if storyWords > 450:
                #Array which will containt story chunks
                summarizerText=[]
                #summuraize story into chunks
                textChunk=round(storyWords/600)
                #print("WORDS", storyWords)
                #print("CHUNK",textChunk)
                #print(np.ceil(len(storyWords)/400))
                endChunk=0
                for i in range (1,textChunk+1):
                    startChunk=endChunk
                    endChunk=round(storyWords/textChunk)*i
                  #  print("start",startChunk)
                    #print("end CHUNK", endChunk)

                    summarizerText.append(storyText.split()[startChunk:endChunk])
                  #  print("sum", summarizerText[i-1])
                    #print(" ".join(summarizerText[i-1]))
                    #print(int(400/textChunk))
                    # summuriazie text to get shorter text which will be fed to model
                    textSummarization=textSummarization+GPT2.sum2(" ".join(summarizerText[i-1]),int(600/textChunk))
                storyText=textSummarization
            print("FINAL SURR",storyText)
            if storyTitle == "Title":
                print("TITLEELELALE", round(len(storyText.split()) + 70 / 0.75))
                storyTitle = GPT2.model('Description:' + storyText + 'Title:',
                                        round((len(storyText.split()) + 50) / 0.75), 1, 10, 'gpt2-TitleGenerator')
                #storyTitle=storyTitle[storyTitle.find('Title:')+len('Title:'):].replace('.','')
                storyTitle=storyTitle.replace('.','')

            else:
                print("Title already generated.")
                #print("Sum",summarizerText)
                #summuriazie text to get shorter text which will be fed to model
            max_length = round((len(storyText.split()) + 300)/ 0.75)
            print("MAX", max_length)
            # Setting Min length slightly lower than Max length
            min_length = max_length - 10

            # Generating text
            storyTest=storyText
            storyText = GPT2.model(storyText, max_length, min_length, 10, "gpt2-medium-N")
            if int(clicked) % 4 == 0:
                storyTextChoice = GPT2.model(storyTest, max_length, min_length, 10, "gpt2-medium-N")
                storySumChoice=GPT2.sum2(storyTextChoice,60)
                storySumChoice1=GPT2.sum2(storyText,60)

                print("KURWA",storySumChoice)
                return{'storyText':storyText,'storySumChoice1':storySumChoice1,'storyTextChoice':storyTextChoice,'storySumChoice':storySumChoice}
            #orginalText+storyText.encode('utf-8')
#replace('\n', '\r\n')

        return {'storyText': storyText, 'storyTitle':storyTitle}
        # return render_template('home.html' )




def run():
    app.run()
