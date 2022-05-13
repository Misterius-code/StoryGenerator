import os
import sys
sys.path.append('modules')

import GPT2
import flaskServer
import FineTuneTitle
import FineTuneModel


if __name__ == '__main__':
    decision=int( input("""   Welcome to Story Generator! Select one of following: 
        1: Text Generation
        2: Fine-tune text genration model
        3: Fine-tune titles
     """))
    if decision == 1:
        flaskServer.run()
    elif decision == 2:
        FineTuneModel.run()
    elif decision == 3:
        FineTuneTitle.run()
 
