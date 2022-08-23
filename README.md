
<h1 align="center"> AI Story Generator </h1> <br>
Final year project for the university which uses all my knowledge I learned on studies. The project is a quite interesting research question, which is:

“Can machine learning be used to modernize electronic books by connecting text generation and user interactions?”. 

This project focuses on the implementation of machine learning transformers algorithms to generate a new text from the original source. The project use machine learning models such as GTP-2 and T5 to generate a book like tales/stories. The main objective of the software is to generate new text which would be a continuation of the previous text. Purpose of it, is to create a book like resemblance from couple texts. 


![image](https://user-images.githubusercontent.com/55873838/186183794-05e75e85-5d77-4aaf-8e42-7052cbead40a.png)


<h1>Technologies used:</h1>
<h4>Python-All the backend and generation functions were writen in Python.</h4>
<h4>Flask-A framework used as a server to send and revice neccesary data from website to model.</h4>
<h4>GPT-2 - Main text generation model in project , responsible for creating new lines of text based of orginal story.</h4>
<h4>T5 -Machine learning model used to summarize stories which were to big to load into GPT-2 model.</h4>
<h4>JavaScript -Mainly responisble for user ineracation and sending data to backend.</h4>


 

<h1>Features:</h1>
<h2>Title Generation</h2>
<h4>Title generation is simplest process of text generation in the whole project therefore a smallest available model from GPT-2 series was assigned for this task. Assigning the GPT-2 Small (117M) model gave a better flexibility and outcomes because model is lighter and quicker than other GPT-2 versions. This model was finte-tuned in order create a accurate title based on the story.
</h4>
  
![image](https://user-images.githubusercontent.com/55873838/186206578-f44e7c08-0e86-4d27-af29-9836912f4d39.png)

<h2 ">Text Generation</h2>
<h4>Program initaly takes a story from the website and depending of the size of the text it either summarize it or place is straight to model. Model generate a new text based on the input and it is capable of generating 250 words every minute. Generated text is mostly coherent and contains a continuation of the previous story.</h4>
<p align="center" >
 

</p>

<h2>Influance options</h2>
<h4></h4>Influence options are one of the most interesting features which generates 2 continuations of story. User needs to select which story line would like to continue. Based on user input a story will go into the one of 2 directions. The only problem is that user would need to wait a little bit longer for story to appear  as it needs to generate 2 stories instead of one. 
<p align="center" >
 
![image](https://user-images.githubusercontent.com/55873838/186211413-dcb3500f-8031-430b-b44e-2ac39cf07908.png)
</p>
<h2>Addational project features which are not descirbed in this file:</h2>
<h4>Main character customization</h4>
<h4>Fine-tuning</h4>
<h4>Advanced Settings</h4>
<h4>Live text edit</h4>
<h4>Summarization</h4>





<h1>Instalation Instrunctions </h1>
Please install all requirements from requirements.txt
As well please make sure to allocate enough space for the project as is quite heavy. 
Please make sure you have enough comupting power (GPU and RAM) to run the project. 
Recomened resources:
Intel i5 10th generation
RTX 3060 GPU with 6GB or memory
16 GB of RAM

Project might not or run much slower if user do not meet those requirments. 

Please make sure CUDA is installed properly of your device. 

Open terminal and move to root of project then use this command:

pip install -r ./requirements.txt

If you encounter any problem with the project, please contanct me on:
4alekm54@solent.ac.uk
or
Quakemisterius@gmail.com
