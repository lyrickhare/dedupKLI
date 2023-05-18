import cv2

def var(imgPath):
    """calculates variance of the image which is a parameter to judge blurryness of image"""
    img = cv2.imread(imgPath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    var = cv2.Laplacian(img, cv2.CV_64F).var()
    return var


def exactSame(img1pth,img2pth):
    """returns 1 if both images are exactly same"""
    if(open(img1pth,"rb").read() == open(img2pth,"rb").read()):
        return 1
    else:
        return 0
    

def bestquality(classifiedDict):
    """
    eg:
    - Input:
        - classifiedDict: \\
            {\\
            'PAN': ['pan.jpg'],\\
            'DL': [ ],\\
            'Passport': [ ],\\
            'Aadhaar': ['aadhar.png', 'aadharlk.png', 'aadharlkb.png'],\\
            'other': ['rand.jpg','rand1.jpg','img.jpg']\\
            }
    - Returns:
        - singleDict: \\
            {\\
            'PAN': ['pan.jpg'],\\
            'DL': [ ],\\
            'Passport': [ ],\\
            'Aadhaar': ['aadhar.png'],\\
            'other': ['rand.jpg', 'img.jpg' ]\\
            }
        
    ----------
    
    - Only keeps the best-quality image in the array
    - Note: for *other* key; it deletes only exactly same images
    as in example 'rand1.jpg' was the copy of 'rand.jpg'
    so it was deleted;
    while 'img.jpg' was a different image
    so it was kept irrespective of it's output


    """
    
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
