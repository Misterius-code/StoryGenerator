from alive_progress import alive_bar
import pdfplumber
import os

def pdf():
    startOfBook= ['Chapter', 'Prologue']

    allbooks = os.listdir("resources\\books\\fantasy\\pdf\\20k")
   # allbooks.remove('desktop.ini')
    allText=""
    for pdfBooks in allbooks:
        file_exists = os.path.exists(f'resources\\books\\Fantasy\\txt\\20k\\{pdfBooks.replace("pdf","txt")}')
        if file_exists:
            print(f'Already Exist: {pdfBooks.replace("pdf","txt")}')
        else:
            print(pdfBooks)
            startofBookFound = False
            pdf = pdfplumber.open(f'resources\\books\\fantasy\\pdf\\20k\\{pdfBooks}')
            # total_pages= len(pdf.pages)
            all_text=""
            with alive_bar(len(pdf.pages)) as bar:
              print("Name:{0} Number of Pages: {1}".format(pdfBooks,len(pdf.pages) ))
              for pdf_page in pdf.pages:
                   single_page_text = pdf_page.extract_text()
                   #if startOfBook in single_page_text:
                   if (single_page_text.find(startOfBook[0]) >=0 or single_page_text.find(startOfBook[1]) >=0) and len(single_page_text.split()) >=150 and startofBookFound == False:
                       all_text=""
                       startofBookFound=True
                       print("YES")
                       print( len(single_page_text.split()))

                   all_text = all_text + '\n' + single_page_text
                   bar()
                   #print("lel")
              print("Book Added")
              with open(f'C:\\Users\\Quake\\Desktop\\StoryGenerator\\resources\\books\\fantasy\\txt\\20k\\{pdfBooks.replace("pdf","txt")}', 'w' ,encoding="utf-8") as text_file:
                print(f"{all_text}", file=text_file)

              allText=allText+"\n <|startoftext|> " + all_text + " <|endoftext|> "
              with open(
                      f'C:\\Users\\Quake\\Desktop\\StoryGenerator\\resources\\books\\fantasy\\txt\\20k\\allText.txt',
                      'w', encoding="utf-8") as text_file1:
                  print(f"{allText}", file=text_file1)
        #page = pdf.pages[0]
        #text = page.extract_text()


       # wordCount = len( all_text.split())
       # print(wordCount)
            pdf.close()


def txt():
    allbooks = os.listdir("resources\\books\\fantasy\\txt\\9k")
    allText=""
    for pdfBooks in allbooks:
        with open(
                f'C:\\Users\\Quake\\Desktop\\StoryGenerator\\resources\\books\\fantasy\\txt\\9k\\{pdfBooks}',
             encoding="utf-8") as all_text:
                      all_text1=all_text.read()


        allText = allText + "\n <|startoftext|> " + all_text1 + " <|endoftext|> "
        with open(
                f'C:\\Users\\Quake\\Desktop\\StoryGenerator\\resources\\books\\fantasy\\txt\\9k\\allText.txt',
                'w', encoding="utf-8") as text_file1:
            print(f"{allText}", file=text_file1)

