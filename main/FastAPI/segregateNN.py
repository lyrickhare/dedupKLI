# Importing classifier class from opclass.py file
from opclass import Classifier 

#creating an object 
modelObj = Classifier()

# Initialising the model to load the weightage file
modelObj.init_model()


def segregate(filepaths):
    """
    uses NN to classify image
    
    eg:
    - Input:
        - filepaths = ["aadhar.png","aadharlk.png","aadharlkb.png","pan.jpg"]
    - Returns:
        - {'PAN': ['pan.jpg'],
        'DL': [ ],
        'Passport': [ ],
        'Aadhaar': ['aadhar.png', 'aadharlk.png', 'aadharlkb.png'],
        'other': [ ]}
    ----------
    Takes an list of imagePaths as Input \\
    and Outputs a dictionary having 5 keys:
    - PAN
    - DL
    - Passport
    - Aadhaar
    - other
    
    with an list of filepaths as values
    
    """
    classifiedDict = {"PAN":[],"DL":[],"Passport":[],"Aadhaar":[],"other":[]}
    for path in filepaths:
        doctype = modelObj.get_prediction(path)
        classifiedDict[doctype].append(path)
        print("addedInClassifieddict")
    return classifiedDict