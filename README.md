# dedupKLI

# Usage steps

- go to "dedupKLI\main"
- check if proposalmod folder is there, if it is then delete it
- now open the proposal folder and add your folder of images in it (for reference you can check proposal1, proposal2 and proposal3)
- now run test.py
- A new folder named proposalmod will be created in the main directory
- This folder will have all the folders that are in proposal and these children folders will contain indexed folders for documents
- The matrix_ parameters will be there in output
![image](https://github.com/lyrickhare/dedupKLI/assets/80460792/b536ecdf-81b7-4a1b-91b8-4a68fd8aded8)


# Dependencies 
- os
- pathlib
- sys
- shutil
- cv2 (opencv)
- numpy
- ftfy
- pytesseract
- tesseract (software)
- PIL
- regex
- fuzzywuzzy
- Levenshtein
