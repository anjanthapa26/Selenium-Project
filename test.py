import re
def readFile(fileName):
    
    getInfo = []
    getExperience = []
    get_tech_stack = []
    tech_stacks = ['AWS', 'Azure', 'Ansible', 'Python', 'Docker', 'Kubernetes', 'Terraform',  'Jenkins',  'Puppet']
    fileObj = open(fileName,'r')
    words = fileObj.read().splitlines()

    for word in words:
        if re.findall('\d+ years',word):
            getExperience.append(re.findall('\d+ years',word)[0])
        if re.findall('\d+ year',word):
            getExperience.append(re.findall('\d+ year',word)[0])
        if re.findall('\d\+ years',word):
            getExperience.append(re.findall('\d\+ years',word)[0])

        for each_char in tech_stacks:
            if each_char in word:
                get_tech_stack.append(each_char)


    if len(getExperience) > 0:
        final_list_of_years = max(list(map(int,re.findall('\d+',' '.join(getExperience)))))
        getInfo.append(final_list_of_years)
    else:
        getInfo.append('N/A')

    getInfo.append(' '.join(get_tech_stack))
    
    for word in words:
        if word.find('U.S') != -1 or word.find('U.S work permit') != -1 or word.find('USA') != -1 or word.find('U.S permit') != -1:
            getInfo.append(True)
            return getInfo

    fileObj.close()

    getInfo.append(False)
    return getInfo

print(readFile('demofile.txt'))