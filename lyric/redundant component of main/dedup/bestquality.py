import cv2

def var(imgPath):
    img = cv2.imread(imgPath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    var = cv2.Laplacian(img, cv2.CV_64F).var()
    return var


def exactSame(img1pth,img2pth):
    if(open(img1pth,"rb").read() == open(img2pth,"rb").read()):
        return 1
    else:
        return 0
    

def bestquality(classifiedDict):
    singleDict = {"PAN":[],"DL":[],"Passport":[],"Aadhaar":[],"other":[]}
    for key in classifiedDict: 
        if(key!="other"):
            varv = 0
            pathv =""
            for path in classifiedDict[key]:
                varc = var(path)
                if (varc>varv):
                    varv = varc
                    pathv = path
            singleDict[key].append(pathv)
        else:
            l = len(classifiedDict["other"])
            singleDict["other"] = classifiedDict["other"]
            pop = set()
            for i in range(l):
                for j in range(i+1,l):
                    if(exactSame(classifiedDict["other"][i],classifiedDict["other"][j])):
                        pop.add(j)
                    else:
                        pass
            for i in sorted(pop, reverse=True):
                del singleDict["other"][i]
    return singleDict
