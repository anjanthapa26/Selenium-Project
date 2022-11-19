import re
def readFile(fileName):
    
    getInfo = []
    getExperience = []
    fileObj = open(fileName,'r')
    words = fileObj.read().splitlines()

    for i in words:
        if re.findall('\d+ years',i):
            getInfo.append(re.findall('\d+ years',i)[0])
            break

    for word in words:
        if word.find('U.S') != -1 or word.find('U.S work permit') != -1 or word.find('USA') != -1 or word.find('U.S permit') != -1:
            getInfo.append(True)
            return getInfo

    fileObj.close()

    getInfo.append(False)
    return getInfo

print(readFile('demofile.txt'))