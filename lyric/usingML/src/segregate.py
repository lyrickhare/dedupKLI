from opclass import Classifier as oc
a=oc()
a.init_model()
def segregate(filepaths):
    classifiedDict = {"PAN":[],"DL":[],"Passport":[],"Aadhaar":[],"other":[]}
    for path in filepaths:
        doctype = a.get_prediction(path)
        classifiedDict[doctype].append(path)
    return classifiedDict