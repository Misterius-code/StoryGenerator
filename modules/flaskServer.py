from flask import Flask, render_template, request,send_file
app = Flask(__name__, template_folder='../webserver/site2', static_folder='../webserver/site2')
import GPT2
import os
import time
import numpy as np
import re


#Main route
@app.route('/')
def home():
    #list all models
    allModels = os.listdir("models")
    #remove title model as it shoudn't be used by user
    allModels.remove("gpt2-TitleGenerator")
    #Print all models without title model
    print("Available Models:" , allModels)
    return render_template('Home.html' , allModels=allModels)


def unpackRequest(request):
    # Take a story from website
    storyText = request.form['text']
    print("Story length in words ", len(storyText.split()))

    # Take a desired lenght of story
    storyLength = request.form['length']
    print("Story limit", storyLength)

    # Story Title
    storyTitle = request.form['title']

    # Check whether button was cliecked
    clicked = request.form['clicked']
    print("Model", clicked)

    # Take desired model
    storyModel = request.form['model']
    print("Model", storyModel)

    # Take topK parameter from website
    topK = request.form['topK']
    print("top_k", topK)

    # Take temperature parameter from website
    temp = request.form['temp']
    print("temp", temp)

    # Lenght of the story counted as words
    storyWords = len(storyText.split())

    return storyText,storyLength,storyTitle,clicked,storyModel,topK,temp,storyWords



#Generate text
@app.route('/generate', methods=['POST'])
def generate():
    if request.method == 'POST':
        #Unpack a request into right variables
        storyText,storyLength,storyTitle,clicked,storyModel,topK,temp,storyWords=unpackRequest(request)

        textSummarization=""
        if storyWords > int(storyLength):
            print("Story reached the limit ")
            return "Story reached the limit"
        else:
            #limit for story length in words before summurization
            if storyWords > 450:

                #Array which will containt story chunks
                summarizeText=[]

                #summuraize story into chunks
                textChunk=round(storyWords/600)
                endChunk=0

                for i in range (1,textChunk+1):
                    startChunk=endChunk
                    endChunk=round(storyWords/textChunk)*i
                    summarizeText.append(storyText.split()[startChunk:endChunk])

                    # summuriazie text to shorter instance of text which will be then feed to text generation model
                    textSummarization=textSummarization+GPT2.sum2(" ".join(summarizeText[i-1]),int(600/textChunk))
                #Summarized text
                storyText=textSummarization

            #Check if story have title
            if storyTitle == "Title":
                #Generate title based on description
                storyTitle = GPT2.model('Description:' + storyText + 'Title:',
                                        round((len(storyText.split()) + 50) / 0.75), 1, 10, 'gpt2-TitleGenerator', 1)

                #Remove dot from title as there are no books with dots in title
                storyTitle=storyTitle.replace('.','')
            else:
                print("Title already generated.")
            #Set up max length
            max_length = round((len(storyText.split()) + 300)/ 0.75)
            # Setting Min length slightly lower than Max length
            min_length = max_length - 10

            # Generating text
            storyText = GPT2.model(storyText, max_length, min_length, topK, storyModel,temp)

            #Every 2 generation create extra two stories and let user decice which he would like to pick
            if int(clicked) % 2 == 0:
                secondChoice = GPT2.model(storyText, max_length, min_length, topK, storyModel,temp)
                secondChoiceSum=GPT2.sum2(secondChoice,30)
                sumChoice=GPT2.sum2(storyText,30)
                return{'storyText':storyText,'sumChoice':sumChoice,'secondChoice':secondChoice,'secondChoiceSum':secondChoiceSum}

            #Possible improvements for text clearity
            #orginalText+storyText.encode('utf-8')
            #replace('\n', '\r\n')

        #return a new generated text and title
        return {'storyText': storyText, 'storyTitle':storyTitle}




#Next page is a button on the website which is responsible for generation next 250 words
@app.route('/nextPage', methods=['POST'])
def nextPage():
    if request.method == 'POST':
        #Recive a request data
        storyText,  storyLength, storyTitle, clicked, storyModel, topK, temp, storyWords = unpackRequest(request)

        regex = r'([A-z][^.!?]*[.!?]*"?)'
        sumChars=""
        i=0
        #Check whether story reached a limit $storyLength
        if storyWords > int(storyLength):
            print("Story reached the limit ")
            storyText=""
            return "Story reached the limit"
        else:
            #if story lenght is lower than requested from user then continue
            print("NEXT PAGE GENERATION")
            #Check whether story is shorter than 600 words
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

                storyText = GPT2.model(storyText, max_length, min_length, topK, storyModel,temp)

                #print(storyArray)
                #print(test1)
                if int(clicked) % 1 == 0:
                    secondChoice = GPT2.model(storyText, max_length, min_length, topK, storyModel,temp)
                    secondChoiceSum = GPT2.sum2(secondChoice, 30)
                    sumChoice = GPT2.sum2(storyText, 30)
                    return {'storyText': storyText, 'sumChoice': sumChoice, 'secondChoice': secondChoice,
                            'secondChoiceSum': secondChoiceSum}
            else:
                max_length = round((len(storyText.split()) + 300) / 0.75)
                # Setting Min length slightly lower than Max length
                min_length = max_length - 10
                # Generating text
                storyText = GPT2.model(storyText, max_length, min_length, topK, storyModel,temp)


    return(storyText)



def run():
    app.run()
