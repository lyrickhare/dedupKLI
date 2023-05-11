import cv2

def var(imgPath):
    img = cv2.imread(imgPath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    var = cv2.Laplacian(img, cv2.CV_64F).var()
    return var


def bestquality(classifiedDict):
    singleDict = {"PAN":[],"DL":[],"Passport":[],"Aadhaar":[],"other":[]}
    for key in classifiedDict: 
        varv = 0
        pathv =""
        for path in classifiedDict[key]:
            varc = var(path)
            if (varc>varv):
                varv = varc
                pathv = path
        singleDict[key].append(pathv)
    return singleDict
