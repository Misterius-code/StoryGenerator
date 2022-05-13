from flask import Flask, render_template, request,send_file
app = Flask(__name__, template_folder='../webserver/site2', static_folder='../webserver/site2')
import GPT2
import os
import time
import numpy as np
import re



@app.route('/')
def home():
    print("Hello World Flask")
    allModels = os.listdir("models")
    print(allModels)
    allModels.remove("gpt2-TitleGenerator")
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
        print("Story length in words ",len(storyText.split()))
        storyLength = request.form['length']
        print("Story limit",storyLength)
        # Gpt-2 model
        storyModel = request.form['model']
        clicked = request.form['clicked']
        storyModel = request.form['model']
        print("Model", storyModel)
        topK = request.form['topK']
        print("top_k", topK)
        temp = request.form['temp']
        print("temp", temp)
        #Lenght of the story in words
        storyWords = len(storyText.split())
        regex = r'([A-z][^.!?]*[.!?]*"?)'
        sumChars=""
        i=0
        if storyWords > int(storyLength):
            print("Story reached the limit ")
            storyText=""
            return "Story reached the limit"
        else:
            print("NEXT PAGE GENERATION")
            if len(storyText)>2600:
                test1=storyText[storyWords-600:]
                storyArray = []
                for sentence in re.findall(regex, storyText):
                    storyArray.append(sentence)
                while len(sumChars)<800:
                    i+=1
                    sumChars=storyArray[-i] +sumChars

                test1 =storyText[len(storyText) - (2600+len(sumChars)):len(storyText)-len(sumChars)]
                storyText=GPT2.sum2(test1,300) + sumChars
               # print(test1)
                max_length = round((len(storyText.split()) + 300) / 0.75)
                min_length = max_length - 10

                storyText = GPT2.model(storyText, max_length, min_length, 10, storyModel)

                #print(storyArray)
                #print(test1)
                if int(clicked) % 1 == 0:
                    secondChoice = GPT2.model(storyText, max_length, min_length, 10, storyModel)
                    secondChoiceSum = GPT2.sum2(secondChoice, 30)
                    sumChoice = GPT2.sum2(storyText, 30)
                    return {'storyText': storyText, 'sumChoice': sumChoice, 'secondChoice': secondChoice,
                            'secondChoiceSum': secondChoiceSum}
            else:
                max_length = round((len(storyText.split()) + 300) / 0.75)
                # Setting Min length slightly lower than Max length
                min_length = max_length - 10
                # Generating text
                storyText = GPT2.model(storyText, max_length, min_length, 10, storyModel)


    return(storyText)




@app.route('/generate', methods=['POST'])
def generate():
    if request.method == 'POST':
        #Get story text from website
        storyText= request.form['text']
        print("Story length in words ",len(storyText.split()))
        # Get story length which should be 2000-5000
        storyLength=request.form['length']
        print("Story limit",storyLength)
        #Story Title
        storyTitle=request.form['title']
        #Gpt-2 model
        storyModel=request.form['model']
        print("Model",storyModel)
        topK=request.form['topK']
        print("top_k",topK)
        temp=request.form['temp']
        print("temp",temp)

        clicked = request.form['clicked']
        #Count how many word have story
        storyWords = len(storyText.split())
        orginalText=storyText
        testText = ""
      #  print(int(storyLength))
        textSummarization=""
        if storyWords > int(storyLength):
            print("Story reached the limit ")
            return "Story reached the limit"
        else:
            #limit for story length in words before summurization
            if storyWords > 450:
                #Array which will containt story chunks
                summarizerText=[]
                #summuraize story into chunks
                textChunk=round(storyWords/600)
                endChunk=0
                for i in range (1,textChunk+1):
                    startChunk=endChunk
                    endChunk=round(storyWords/textChunk)*i
                    summarizerText.append(storyText.split()[startChunk:endChunk])
                    # summuriazie text to get shorter text which will be fed to model
                    textSummarization=textSummarization+GPT2.sum2(" ".join(summarizerText[i-1]),int(600/textChunk))
                storyText=textSummarization
           # print("FINAL SURR",storyText)
            if storyTitle == "Title":
               # print("TITLEELELALE", round(len(storyText.split()) + 70 / 0.75))
                storyTitle = GPT2.model('Description:' + storyText + 'Title:',
                                        round((len(storyText.split()) + 50) / 0.75), 1, 10, 'gpt2-TitleGenerator')
                #storyTitle=storyTitle[storyTitle.find('Title:')+len('Title:'):].replace('.','')
                storyTitle=storyTitle.replace('.','')
            else:
                print("Title already generated.")
                #print("Sum",summarizerText)
                #summuriazie text to get shorter text which will be fed to model
            max_length = round((len(storyText.split()) + 300)/ 0.75)
           # print("MAX", max_length)
            # Setting Min length slightly lower than Max length
            min_length = max_length - 10
            # Generating text
            storyTest=storyText
            storyText = GPT2.model(storyText, max_length, min_length, 10, storyModel)
            if int(clicked) % 2 == 0:
             #   print("PART 2")
                secondChoice = GPT2.model(storyTest, max_length, min_length, 10, storyModel)
                secondChoiceSum=GPT2.sum2(secondChoice,30)
                sumChoice=GPT2.sum2(storyText,30)
                return{'storyText':storyText,'sumChoice':sumChoice,'secondChoice':secondChoice,'secondChoiceSum':secondChoiceSum}
            #orginalText+storyText.encode('utf-8')
#replace('\n', '\r\n')

        return {'storyText': storyText, 'storyTitle':storyTitle}
        # return render_template('home.html' )




def run():
    app.run()
